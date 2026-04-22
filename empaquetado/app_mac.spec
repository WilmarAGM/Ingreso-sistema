# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['../launcher.py'],
    pathex=['..', '.'],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
    ],
    hiddenimports=[
        'engineio.async_drivers.threading',
        'flask_socketio',
        'engineio',
        'socketio',
        'pandas',
        'openpyxl',
        'xlrd',
        'selenium',
        'selenium.webdriver',
        'selenium.webdriver.chrome',
        'selenium.webdriver.chrome.webdriver',
        'selenium.webdriver.chrome.service',
        'selenium.webdriver.chrome.options',
        'selenium.webdriver.chromium',
        'selenium.webdriver.chromium.webdriver',
        'selenium.webdriver.common.driver_finder',
        'selenium.webdriver.common.selenium_manager',
        'selenium.webdriver.common.service',
        'selenium.webdriver.common.by',
        'selenium.webdriver.remote.webdriver',
        'selenium.webdriver.remote.command',
        'selenium.webdriver.remote.errorhandler',
        'selenium.webdriver.support.ui',
        'selenium.webdriver.support.expected_conditions',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='IngresoNotas',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='IngresoNotas',
)

app = BUNDLE(
    coll,
    name='IngresoNotas.app',
    icon=None,
    bundle_identifier='co.unal.ingreso-notas',
    info_plist={
        'CFBundleDisplayName': 'Ingreso de Notas',
        'CFBundleName': 'IngresoNotas',
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': True,
        'LSUIElement': False,
    },
)
