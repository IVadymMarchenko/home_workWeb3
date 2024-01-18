import threading
from pathlib import Path
import shutil
from Dict_types import known_extensions

lock = threading.Lock()

processed_files = set()  # Словарь для отслеживания обраб файлов

def move_files(source_path, destination_path):
    source_path = Path(source_path)
    destination_path = Path(destination_path)
    destination_file = destination_path / source_path.name

    with lock:
        try:
            shutil.move(str(source_path), str(destination_file))
            processed_files.add(source_path)  # Помечаем файл как обработанный
        except FileNotFoundError:
            print(f"Не відомий файл: {source_path}")


def iter_and_move_files(path, category):
    path_dir = Path(path)
    for elem in path_dir.glob("**/*"):
        if elem.is_file() and elem not in processed_files:  # Проверяем, не был ли файл обработан другим потоком
            for key, value in known_extensions.items():
                if elem.suffix in value and key == category:
                    new_dir = path_dir / key
                    new_dir.mkdir(parents=True, exist_ok=True)
                    move_files(elem, new_dir)


def iter_dir_unknown(path):
    path_dir = Path(path)
    for elem in path_dir.glob("**/*"):
        if elem.is_file() and elem not in processed_files:  # Проверяем, не был ли файл обработан другим потоком
            known_extension_found = False
            for key, value in known_extensions.items():
                if elem.suffix in value:
                    known_extension_found = True
                    break

            if not known_extension_found:
                directory = path_dir / 'unknown'
                directory.mkdir(parents=True, exist_ok=True)
                move_files(elem, directory)


def process_dir(path_dir):
    threads = []
    path_way = Path(path_dir)


    # Створюемо потоки для кожної категорії
    for category in known_extensions.keys():
        thread = threading.Thread(target=iter_and_move_files, args=(path_dir, category))
        threads.append(thread)

    # Создаем потік для невідомих файлів
    unknown_thread = threading.Thread(target=iter_dir_unknown, args=(path_dir,))
    threads.append(unknown_thread)


    # Запускаємо всі потоки
    for thread in threads:
        thread.start()

    # Чекаємо, доки всі потоки завершаться
    for thread in threads:
        thread.join()

    # Видаляємо порожні папки та ті, що містять порожні папки
    for elem in sorted(path_way.glob("**/*"), key=lambda x: len(x.parts), reverse=True):
        if elem.is_dir() and not list(elem.iterdir()):
            shutil.rmtree(elem)

    print('Файли сортовані')

process_dir('D:\Хлам')