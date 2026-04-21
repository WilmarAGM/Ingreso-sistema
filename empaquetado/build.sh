#!/bin/bash
# Script para empaquetar en Linux
echo "Instalando dependencias necesarias..."
pip install pyinstaller eventlet
pip install -r requirements.txt

echo "Iniciando empaquetado con PyInstaller..."
pyinstaller --noconfirm --onefile --windowed \
    --hidden-import "engineio.async_drivers.threading" \
    --add-data "templates:templates" \
    --add-data "static:static" \
    app.py

echo "Proceso finalizado. El ejecutable estará en la carpeta 'dist/'"
