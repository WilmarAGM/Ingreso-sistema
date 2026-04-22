#!/bin/bash
# Ejecutar este script en macOS
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$SCRIPT_DIR/dist_mac"
OUTPUT_DIR="$SCRIPT_DIR/IngresoNotas-Mac"

echo "======================================"
echo " Build macOS - IngresoNotas"
echo "======================================"

if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "ERROR: Este script debe ejecutarse en macOS"
    exit 1
fi

cd "$PROJECT_DIR"

echo ""
echo "[1/5] Instalando dependencias de empaquetado..."
pip3 install pyinstaller -q
pip3 install -r requirements.txt -q

echo ""
echo "[2/5] Empaquetando con PyInstaller..."
pyinstaller --noconfirm \
    "$SCRIPT_DIR/app_mac.spec" \
    --distpath "$DIST_DIR" \
    --workpath "$SCRIPT_DIR/build_mac"

echo ""
echo "[3/5] Preparando carpeta de entrega..."
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"
cp -r "$DIST_DIR/IngresoNotas.app" "$OUTPUT_DIR/IngresoNotas.app"

echo ""
echo "[4/5] Creando DMG (instalar.dmg)..."

# Carpeta temporal con .app + enlace a /Applications
TEMP_DMG="$(mktemp -d)"
cp -r "$OUTPUT_DIR/IngresoNotas.app" "$TEMP_DMG/IngresoNotas.app"
ln -s /Applications "$TEMP_DMG/Applications"

hdiutil create \
    -volname "Ingreso de Notas" \
    -srcfolder "$TEMP_DMG" \
    -ov \
    -format UDZO \
    "$OUTPUT_DIR/instalar.dmg"

rm -rf "$TEMP_DMG"

echo ""
echo "[5/5] Creando ZIP para distribución..."
cd "$SCRIPT_DIR"
rm -f IngresoNotas-Mac.zip
zip -r "IngresoNotas-Mac.zip" "IngresoNotas-Mac/"

echo ""
echo "======================================"
echo " LISTO"
echo "======================================"
echo " Carpeta: $OUTPUT_DIR"
echo " ZIP:     $SCRIPT_DIR/IngresoNotas-Mac.zip"
echo ""
echo " Estructura:"
echo "   IngresoNotas-Mac/"
echo "   ├── IngresoNotas.app   (la aplicación)"
echo "   └── instalar.dmg       (imagen de disco para instalar)"
echo ""
echo " El DMG muestra IngresoNotas.app + carpeta Applications"
echo " El usuario arrastra la app a Applications para instalar."
echo ""
echo " NOTA: En Mac sin firma de código el usuario debe ir a:"
echo "   Ajustes del Sistema > Privacidad y Seguridad > Abrir de todas formas"
echo ""
