import os
import sys
import subprocess
import shutil

# Получаем текущую директорию скрипта
current_dir = os.path.dirname(os.path.abspath(__file__))

# Очищаем предыдущие сборки
dist_dir = os.path.join(current_dir, 'dist')
build_dir = os.path.join(current_dir, 'build')

if os.path.exists(dist_dir):
    try:
        shutil.rmtree(dist_dir)
        print(f"Удалена директория: {dist_dir}")
    except Exception as e:
        print(f"Ошибка при удалении {dist_dir}: {e}")

if os.path.exists(build_dir):
    try:
        shutil.rmtree(build_dir)
        print(f"Удалена директория: {build_dir}")
    except Exception as e:
        print(f"Ошибка при удалении {build_dir}: {e}")

# Запускаем PyInstaller
spec_file = os.path.join(current_dir, 'warehouse_app.spec')
cmd = [sys.executable, '-m', 'PyInstaller', spec_file, '--clean']

try:
    print("Запуск сборки приложения...")
    subprocess.run(cmd, check=True)
    print("\nСборка успешно завершена!")
    print(f"Исполняемый файл находится в: {os.path.join(dist_dir, 'WarehouseSystem.exe')}")
except subprocess.CalledProcessError as e:
    print(f"\nОшибка при сборке: {e}")
except Exception as e:
    print(f"\nНеизвестная ошибка: {e}") 