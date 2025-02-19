import logging
import os
import threading
from datetime import datetime


class CustomLogger:
    """Кастомный логгер"""

    def __init__(self, path_to_folder: str = None, flow_name: str = None, console_output: bool = True) -> None:
        """
        Инициализация параметров

        Args:
            path_to_folder (str, optional): путь до папки. Defaults to None.
            flow_name (str, optional): имя потока для логирования. Defaults to None.
            console_output (bool, optional): вывод информации в консоль (True or False). Defaults to True.
        """
        self.name_folder = 'Log'
        self.current_day = datetime.now().strftime("%d.%m.%Y")

        if path_to_folder:
            self.path_to_folder = os.path.join(os.getcwd(), path_to_folder, self.name_folder)
        else:
            self.path_to_folder = os.path.join(os.getcwd(), self.name_folder)
        self._check_folder_for_log_file()

        if flow_name:
            self.path_to_file = os.path.join(self.path_to_folder, f'{flow_name}.log')
        else:
            current_day_and_time = datetime.now().strftime("%d.%m.%Y")
            self.path_to_file = os.path.join(self.path_to_folder, f'{current_day_and_time}.log')

        self.log = logging.getLogger(self.path_to_file)

        if not console_output:
            self.console_handler = False
        else:
            self.console_handler = self._setting_for_log_formatter_console()
            self.log.addHandler(self.console_handler)

        self.file_handler = self._setting_for_log_formatter_file()
        self.log.addHandler(self.file_handler)

        self.log.setLevel(logging.DEBUG)

    def _check_folder_for_log_file(self) -> None:
        """Создание директории для логирования"""
        if not os.path.exists(self.path_to_folder):
            os.makedirs(self.path_to_folder, exist_ok=True)

    def _setting_for_log_formatter_file(self) -> object:
        """Настройка для формата записи файла *.log"""
        file_formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)s] - [%(filename)s] - %(funcName)s: (%(lineno)d) - %(message)s')
        file_handler = logging.FileHandler(self.path_to_file, encoding='UTF-8')
        file_handler.setFormatter(file_formatter)

        return file_handler

    def _setting_for_log_formatter_console(self) -> object:
        """Настройка для вывода данных в консоль"""
        console_formatter = logging.Formatter('[%(asctime)s] - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)

        return console_handler

    def close_logger(self) -> None:
        """Общее закрытие обработчиков (файл, консоль) и удаление их из логгера"""
        self.file_handler.close()
        self.log.removeHandler(self.file_handler)

        if self.console_handler:
            self.console_handler.close()
            self.log.removeHandler(self.console_handler)

    def get_path_to_file_log(self) -> str:
        """Возвращает полный путь до файла логгера"""
        return self.path_to_file

    def start_initialization(self) -> object:
        """Запуск логгера"""
        return self.log
