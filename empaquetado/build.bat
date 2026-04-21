@echo off
:: Script para empaquetar en Windows
echo Instalando dependencias necesarias...
pip install pyinstaller eventlet
pip install -r requirements.txt

echo Iniciando empaquetado con PyInstaller...
pyinstaller --noconfirm --onefile --windowed ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    app.py

echo Proceso finalizado. El ejecutable estara en la carpeta 'dist/'
pause
