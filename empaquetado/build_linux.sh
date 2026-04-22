#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$SCRIPT_DIR/dist_linux"
OUTPUT_DIR="$SCRIPT_DIR/IngresoNotas-Linux"

echo "======================================"
echo " Build Linux - IngresoNotas"
echo "======================================"

cd "$PROJECT_DIR"

echo ""
echo "[1/5] Instalando dependencias de empaquetado..."
pip install pyinstaller -q
pip install -r requirements.txt -q

echo ""
echo "[2/5] Empaquetando con PyInstaller (onedir)..."
pyinstaller --noconfirm \
    "$SCRIPT_DIR/app_linux.spec" \
    --distpath "$DIST_DIR" \
    --workpath "$SCRIPT_DIR/build_linux"

echo ""
echo "[3/5] Preparando carpeta de entrega..."
rm -rf "$OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# La carpeta del build pasa a llamarse IngresoNotas.app
cp -r "$DIST_DIR/IngresoNotas" "$OUTPUT_DIR/IngresoNotas.app"
chmod +x "$OUTPUT_DIR/IngresoNotas.app/IngresoNotas"

echo ""
echo "[4/5] Copiando instalador..."
cp "$SCRIPT_DIR/instalar_linux.sh" "$OUTPUT_DIR/instalar.sh"
chmod +x "$OUTPUT_DIR/instalar.sh"

echo ""
echo "[5/5] Creando ZIP para distribución..."
cd "$SCRIPT_DIR"
rm -f IngresoNotas-Linux.zip
zip -r "IngresoNotas-Linux.zip" "IngresoNotas-Linux/"

echo ""
echo "======================================"
echo " LISTO"
echo "======================================"
echo " Carpeta: $OUTPUT_DIR"
echo " ZIP:     $SCRIPT_DIR/IngresoNotas-Linux.zip"
echo ""
echo " Estructura:"
echo "   IngresoNotas-Linux/"
echo "   ├── IngresoNotas.app/   (carpeta con el programa)"
echo "   └── instalar.sh         (ejecutar para instalar)"
echo ""
