@echo off
echo Instalando dependencias necesarias...
pip install pyinstaller
pip install -r requirements.txt

echo Iniciando empaquetado con PyInstaller...
pyinstaller --noconfirm app.spec

echo Proceso finalizado. El ejecutable estara en la carpeta 'dist/'
pause
