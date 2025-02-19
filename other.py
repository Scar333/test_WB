import csv
import os


def create_folder(path_to_folder: str) -> None:
    """Создание директории"""

    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder, exist_ok=True)


def read_csv_without_header(file_path: str) -> list | None:
    """
    Чтение csv файла с url

    :param file_path: Путь до csv файла

    :return: Список данных из csv файла
    """

    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.extend(row)
    return data


def list_files_in_directory(path_to_folder: str) -> list:
    """
    Возвращает список всех файлов в указанной директории с полными путями.

    :param path_to_folder: Путь к директории.
    :return: Список файлов в директории с полными путями.
    """
    try:
        all_entries = os.listdir(path_to_folder)
        files = []
        for entry in all_entries:
            full_path = os.path.join(path_to_folder, entry)
            if os.path.isfile(full_path):
                files.append(full_path)

        return files

    except Exception as e:
        print(f"Произошла ошибка при чтении директории {path_to_folder}! Ошибка:\n{e}")
        return []
