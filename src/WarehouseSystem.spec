# -*- mode: python ; coding: utf-8 -*-

import os

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Добавление ресурсов, шрифтов и других файлов
        ('fonts', 'fonts'),
        ('resources', 'resources')
    ],
    hiddenimports=[
        'main_window',
        'login_window',
        'auth_service',
        'database',
        'styles',
        'dialogs',
        'visualization',
        'data_export',
        'validators',
        'tabs.products_tab',
        'tabs.stock_tab',
        'tabs.orders_tab',
        'tabs.suppliers_tab',
        'tabs.warehouses_tab'
    ],
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
    name='WarehouseSystem',
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
)
