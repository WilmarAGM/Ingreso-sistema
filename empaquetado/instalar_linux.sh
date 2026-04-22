#!/bin/bash

APP_DIR="$(cd "$(dirname "$0")/IngresoNotas.app" && pwd)"
EJECUTABLE="$APP_DIR/IngresoNotas"
INSTALL_DIR="$HOME/.local/share/IngresoNotas"
LAUNCHER="$HOME/.local/bin/ingreso-notas"
DESKTOP="$HOME/.local/share/applications/ingreso-notas.desktop"
DESKTOP_SHORTCUT="$HOME/Escritorio/Ingreso de Notas.desktop"

# -------------------------------------------------------------------
mostrar() { echo "[IngresoNotas] $*"; }
error()   { echo "[ERROR] $*" >&2; exit 1; }
# -------------------------------------------------------------------

mostrar "=== Instalador de Ingreso de Notas ==="
echo ""

# 1. Verificar que la carpeta .app existe
if [ ! -f "$EJECUTABLE" ]; then
    error "No se encontró '$EJECUTABLE'. Asegúrate de ejecutar instalar.sh desde la misma carpeta donde está IngresoNotas.app"
fi

# 2. Verificar Chrome o Chromium
mostrar "Verificando Google Chrome / Chromium..."
CHROME_OK=false
for cmd in google-chrome google-chrome-stable chromium chromium-browser; do
    if command -v "$cmd" &>/dev/null; then
        CHROME_OK=true
        mostrar "  Encontrado: $cmd"
        break
    fi
done

if [ "$CHROME_OK" = false ]; then
    mostrar "Chrome/Chromium no encontrado. Intentando instalar Chromium..."
    if command -v apt-get &>/dev/null; then
        sudo apt-get update -qq && sudo apt-get install -y chromium-browser chromium-chromedriver 2>/dev/null \
            || sudo apt-get install -y chromium chromium-driver 2>/dev/null \
            || mostrar "ADVERTENCIA: No se pudo instalar Chromium automáticamente. Instálalo manualmente."
    elif command -v dnf &>/dev/null; then
        sudo dnf install -y chromium 2>/dev/null \
            || mostrar "ADVERTENCIA: No se pudo instalar Chromium. Instálalo manualmente."
    else
        mostrar "ADVERTENCIA: Instala Google Chrome o Chromium manualmente antes de usar la aplicación."
    fi
fi

# 3. Verificar ChromeDriver
mostrar "Verificando ChromeDriver..."
if ! command -v chromedriver &>/dev/null; then
    mostrar "  ChromeDriver no encontrado en PATH."
    if command -v apt-get &>/dev/null; then
        sudo apt-get install -y chromium-chromedriver 2>/dev/null \
            || sudo apt-get install -y chromium-driver 2>/dev/null \
            || mostrar "  ADVERTENCIA: Instala chromedriver manualmente (debe coincidir con la versión de Chrome)."
    fi
fi

# 4. Copiar la aplicación
mostrar "Instalando aplicación en $INSTALL_DIR..."
rm -rf "$INSTALL_DIR"
cp -r "$APP_DIR" "$INSTALL_DIR"
chmod +x "$INSTALL_DIR/IngresoNotas"

# 5. Crear lanzador en ~/.local/bin
mkdir -p "$HOME/.local/bin"
cat > "$LAUNCHER" <<'EOF'
#!/bin/bash
INSTALL_DIR="$HOME/.local/share/IngresoNotas"
cd "$INSTALL_DIR"
"$INSTALL_DIR/IngresoNotas"
EOF
chmod +x "$LAUNCHER"

# 6. Crear entrada en el menú de aplicaciones
mkdir -p "$(dirname "$DESKTOP")"
cat > "$DESKTOP" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Ingreso de Notas
Comment=Sistema de ingreso de notas UNAL
Exec=$LAUNCHER
Icon=applications-education
Terminal=true
StartupNotify=true
Categories=Education;
EOF
chmod +x "$DESKTOP"

# 7. Acceso directo en el escritorio (Gnome/KDE)
for escritorio in "$HOME/Escritorio" "$HOME/Desktop"; do
    if [ -d "$escritorio" ]; then
        cp "$DESKTOP" "$escritorio/Ingreso de Notas.desktop"
        chmod +x "$escritorio/Ingreso de Notas.desktop"
        gio set "$escritorio/Ingreso de Notas.desktop" metadata::trusted true 2>/dev/null || true
        mostrar "  Acceso directo creado en: $escritorio"
    fi
done

# 8. Agregar ~/.local/bin al PATH si no está
if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.profile" 2>/dev/null || true
fi

echo ""
mostrar "=== Instalación completada ==="
echo ""
echo "  Para iniciar la aplicación:"
echo "  - Usa el ícono 'Ingreso de Notas' en el escritorio, o"
echo "  - Ejecuta en terminal: ingreso-notas"
echo ""
echo "  La aplicación abrirá automáticamente el navegador en http://127.0.0.1:5000"
echo "  Para cerrarla, cierra la ventana de terminal que aparece."
echo ""
