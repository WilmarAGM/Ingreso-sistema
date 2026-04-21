# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_all

selenium_datas, selenium_binaries, selenium_hiddenimports = collect_all('selenium')

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=selenium_binaries,
    datas=[('templates', 'templates'), ('static', 'static')] + selenium_datas,
    hiddenimports=[
        'engineio.async_drivers.threading',
    ] + selenium_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Ícono por plataforma (opcional, descomenta si tienes el archivo)
    # icon='static/icon.ico',  # Windows
    # icon='static/icon.icns', # macOS
)

# Bundle .app para macOS
if sys.platform == 'darwin':
    app_bundle = BUNDLE(
        exe,
        name='Ingreso de Notas.app',
        # icon='static/icon.icns',
        bundle_identifier='co.unal.ingreso-notas',
    )
