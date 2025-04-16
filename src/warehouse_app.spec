# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Получаем текущую директорию
current_dir = os.path.dirname(os.path.abspath('G:/Develop/WareHouse_FS_v2/src/warehouse_app.spec'))

# Собираем все подмодули из проекта
hidden_imports = [
    'main_window', 
    'login_window', 
    'auth_service', 
    'database', 
    'styles', 
    'dialogs', 
    'visualization', 
    'data_export', 
    'validators'
]

# Добавляем модули из папки tabs
tabs_dir = os.path.join(current_dir, 'tabs')
if os.path.exists(tabs_dir):
    for item in os.listdir(tabs_dir):
        if item.endswith('.py'):
            module_name = f'tabs.{item[:-3]}'
            hidden_imports.append(module_name)

# Собираем данные файлы из ресурсов
datas = []
# Добавляем папку resources
resources_dir = os.path.join(current_dir, 'resources')
if os.path.exists(resources_dir):
    datas.append(('resources', 'resources'))
# Добавляем папку fonts
fonts_dir = os.path.join(current_dir, 'fonts')
if os.path.exists(fonts_dir):
    datas.append(('fonts', 'fonts'))

a = Analysis(
    ['main.py'],
    pathex=[current_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WarehouseSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Оконный режим без консоли
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
) 