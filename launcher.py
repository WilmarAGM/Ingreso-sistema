# -*- coding: utf-8 -*-
import os
import sys
import threading
import webbrowser
import time

if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
    os.chdir(base_dir)

from app import socketio, app


def _abrir_navegador():
    time.sleep(2.0)
    webbrowser.open('http://127.0.0.1:5000')


threading.Thread(target=_abrir_navegador, daemon=True).start()
socketio.run(app, host='127.0.0.1', port=5000, debug=False, use_reloader=False, allow_unsafe_werkzeug=True)
