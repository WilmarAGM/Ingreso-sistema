import os
import sys
import uuid
import json
import base64
import secrets
import logging
import threading
import io
import queue
import webbrowser
from datetime import timedelta
from threading import Timer

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, join_room
from bot_engine import GradeBot
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Configuración para PyInstaller
if getattr(sys, 'frozen', False):
    # Si el script está "congelado" (ejecutable), los archivos están en sys._MEIPASS
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)
# En ejecutables PyInstaller, la detección automática puede fallar por imports dinámicos.
# Forzamos un modo compatible y estable para evitar "Invalid async_mode specified".
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    manage_session=True,
    async_mode="threading"
)

active_bots = {}
active_bots_lock = threading.Lock()

# Mapa user_id → socket SID real
user_to_socket = {}
user_to_socket_lock = threading.Lock()

# Cola de logs y resultados por usuario (canal de polling)
user_log_queues: dict[str, queue.Queue] = {}
user_results: dict[str, dict] = {}
poll_lock = threading.Lock()


def emit_to_user(user_id, event, data):
    """Emite a un usuario usando su socket SID real como destino primario."""
    with user_to_socket_lock:
        socket_id = user_to_socket.get(user_id)
    if socket_id:
        socketio.emit(event, data, to=socket_id, namespace='/')
        logger.info(f"emit '{event}' → socket={socket_id[:8]}…")
    else:
        # Fallback: room (puede funcionar si el join_room del connect sí corrió)
        socketio.emit(event, data, room=user_id, namespace='/')
        logger.warning(f"emit '{event}' via room fallback (sin socket_id registrado)")


@app.before_request
def make_session_permanent():
    session.permanent = True
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        logger.info(f"Nueva sesión creada: {session['user_id']}")


def get_current_bot():
    sid = session.get('user_id')
    with active_bots_lock:
        if sid and sid in active_bots:
            return active_bots[sid]
    logger.warning(f"Bot no encontrado para SID: {sid}")
    return None


@app.route('/')
def index():
    return render_template('index.html')


# ── SOCKET EVENTS ──────────────────────────────────────────────────────────────

@socketio.on('connect')
def handle_connect():
    """Intento inicial de unir al room. Puede fallar si la sesión no está disponible."""
    user_id = session.get('user_id')
    socket_id = request.sid
    if user_id:
        join_room(user_id)
        with user_to_socket_lock:
            user_to_socket[user_id] = socket_id
        logger.info(f"connect: socket={socket_id[:8]}… → user={user_id[:8]}…")
    else:
        logger.warning(f"connect: socket={socket_id[:8]}… sin user_id en sesión")


@socketio.on('register')
def handle_register(_data=None):
    """
    El cliente envía este evento justo después de conectar para garantizar
    el registro del socket SID incluso si el evento connect no leyó la sesión.
    """
    user_id = session.get('user_id')
    socket_id = request.sid
    if user_id:
        join_room(user_id)
        with user_to_socket_lock:
            user_to_socket[user_id] = socket_id
        logger.info(f"register: socket={socket_id[:8]}… → user={user_id[:8]}…")
        socketio.emit('registered', {'ok': True}, to=socket_id, namespace='/')
    else:
        logger.warning(f"register: socket={socket_id[:8]}… sin user_id")


@socketio.on('disconnect')
def handle_disconnect():
    user_id = session.get('user_id')
    if user_id:
        with user_to_socket_lock:
            user_to_socket.pop(user_id, None)
        logger.info(f"disconnect: user={user_id[:8]}…")


# ── HTTP ROUTES ────────────────────────────────────────────────────────────────

@app.route('/login', methods=['POST'])
def login():
    sid = session.get('user_id')
    if not sid:
        session['user_id'] = str(uuid.uuid4())
        sid = session['user_id']

    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"success": False, "error": "Faltan credenciales"})

    try:
        with active_bots_lock:
            bot = active_bots.get(sid)
        if bot:
            try:
                bot.close()
            except Exception:
                pass

        new_bot = GradeBot(headless=True)

        def status_callback(msg):
            emit_to_user(sid, 'login_status', {'message': msg})

        new_bot.login(username, password, status_callback=status_callback)
        with active_bots_lock:
            active_bots[sid] = new_bot

        groups = new_bot.get_groups_list()
        return jsonify({"success": True, "groups": groups})

    except Exception as e:
        logger.error(f"Error en login para SID {sid}: {e}", exc_info=True)
        screenshot_base64 = ""
        try:
            ss_path = os.path.join(os.getcwd(), "error_login.png")
            if os.path.exists(ss_path):
                with open(ss_path, "rb") as f:
                    screenshot_base64 = base64.b64encode(f.read()).decode('utf-8')
        except Exception:
            pass

        return jsonify({
            "success": False,
            "error": f"Error de conexión o credenciales: {str(e)}",
            "screenshot": screenshot_base64
        })


@app.route('/select_group', methods=['POST'])
def select_group():
    bot = get_current_bot()
    data = request.json
    group_id = data.get('group_id')

    if not bot:
        return jsonify({"success": False, "error": "Sesión no iniciada"})

    try:
        bot.return_to_menu()
        bot.enter_group(group_id)
        options = bot.get_grading_options()
        return jsonify({"success": True, "options": options})
    except Exception as e:
        logger.error(f"Error al seleccionar grupo: {e}", exc_info=True)
        return jsonify({"success": False, "error": str(e)})


@app.route('/get_columns', methods=['POST'])
def get_columns():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No se subió ningún archivo"})

    file = request.files['file']
    try:
        content = file.read()
        ext = os.path.splitext(file.filename)[1].lower()
        if ext == '.csv':
            df = pd.read_csv(io.BytesIO(content))
        elif ext in ['.xls', '.xlsx', '.xlsm']:
            df = pd.read_excel(io.BytesIO(content))
        else:
            return jsonify({"success": False, "error": "Formato no soportado"})

        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        numeric_cols = [c for c in numeric_cols if str(c).lower() != 'documento']
        return jsonify({"success": True, "columns": numeric_cols})
    except Exception as e:
        logger.error(f"Error al leer columnas: {e}", exc_info=True)
        return jsonify({"success": False, "error": str(e)})


@app.route('/process', methods=['POST'])
def process():
    bot = get_current_bot()
    sid = session.get('user_id')

    if not bot:
        return jsonify({"success": False, "error": "Sesión no iniciada"})
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No se subió ningún archivo"})

    file = request.files['file']
    mappings_json = request.form.get('mappings')

    if not mappings_json:
        return jsonify({"success": False, "error": "Faltan mapeos de calificación"})

    try:
        exam_mappings = json.loads(mappings_json)
    except json.JSONDecodeError:
        return jsonify({"success": False, "error": "Formato de mapeo inválido"})

    temp_dir = os.path.join(os.getcwd(), "temp_uploads")
    os.makedirs(temp_dir, exist_ok=True)
    filename = f"{sid}_{file.filename}"
    file_path = os.path.join(temp_dir, filename)
    file.save(file_path)

    try:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext == '.csv':
            df = pd.read_csv(file_path)
        elif ext in ['.xls', '.xlsx', '.xlsm']:
            df = pd.read_excel(file_path)
        else:
            return jsonify({"success": False, "error": "Formato no soportado"})

        with poll_lock:
            user_log_queues[sid] = queue.Queue()
            user_results.pop(sid, None)

        def push_log(msg):
            logger.info(f"[BOT] {msg}")
            with poll_lock:
                if sid in user_log_queues:
                    user_log_queues[sid].put(msg)
            emit_to_user(sid, 'bot_log', {'message': msg})

        def run_bot_task():
            try:
                results_list = bot.start_grading(exam_mappings, df, push_log)
                if results_list:
                    push_log("🎉 ¡PROCESO MULTI-NOTA FINALIZADO!")
                    with poll_lock:
                        user_results[sid] = {'success': True, 'stats_list': results_list}
                    emit_to_user(sid, 'process_complete', {'success': True, 'stats_list': results_list})
                else:
                    push_log("❌ El proceso se detuvo sin resultados.")
                    with poll_lock:
                        user_results[sid] = {'success': False}
                    emit_to_user(sid, 'process_complete', {'success': False})
            except Exception as e:
                logger.error(f"Error en tarea de bot para SID {sid}: {e}", exc_info=True)
                push_log(f"❌ Error crítico: {str(e)}")
                with poll_lock:
                    user_results[sid] = {'success': False}
                emit_to_user(sid, 'process_complete', {'success': False})
            finally:
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except OSError:
                        pass

        t = threading.Thread(target=run_bot_task, daemon=True)
        t.start()
        return jsonify({"success": True})

    except Exception as e:
        logger.error(f"Error al iniciar proceso: {e}", exc_info=True)
        return jsonify({"success": False, "error": str(e)})


@app.route('/poll_status')
def poll_status():
    sid = session.get('user_id')
    if not sid:
        return jsonify({"logs": [], "done": False, "result": None})

    logs = []
    with poll_lock:
        q = user_log_queues.get(sid)
        if q:
            while not q.empty():
                try:
                    logs.append(q.get_nowait())
                except queue.Empty:
                    break
        result = user_results.pop(sid, None)

    return jsonify({
        "logs": logs,
        "done": result is not None,
        "result": result
    })


@app.route('/return_menu', methods=['POST'])
def return_menu():
    bot = get_current_bot()
    if not bot:
        return jsonify({"success": False, "error": "Sesión no iniciada"})

    try:
        bot.return_to_menu()
        groups = bot.get_groups_list()
        return jsonify({"success": True, "groups": groups})
    except Exception as e:
        logger.error(f"Error al volver al menú: {e}", exc_info=True)
        return jsonify({"success": False, "error": str(e)})


@app.route('/logout', methods=['POST'])
def logout():
    sid = session.get('user_id')
    with active_bots_lock:
        bot = active_bots.pop(sid, None)
    if bot:
        try:
            bot.close()
        except Exception:
            pass
    return jsonify({"success": True})


def open_browser():
    """Abre el navegador automáticamente después de 1 segundo."""
    webbrowser.open_new('http://127.0.0.1:5000/')


if __name__ == '__main__':
    # Solo abrimos el navegador si no estamos en modo reloader de Flask
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        Timer(1, open_browser).start()
    
    # En producción (ejecutable) desactivamos debug
    socketio.run(app, host='127.0.0.1', port=5000, debug=False, allow_unsafe_werkzeug=True)
