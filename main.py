from threading import Thread

from _logger import CustomLogger
from config import CONFIG, CONFIG_TV
from link_collection import Wildberries
from other import read_csv_without_header, list_files_in_directory
from pars_data_product import WildberriesProduct
from work_with_excel import write_data_to_excel_wireBank
from work_with_pdf import PDF


def process_url(url_data: str, log: CustomLogger) -> None:
    """
    Запуск обработки URL для потоков.

    :param url_data: URL для обработки.
    :param log: Объект логгера.
    """
    WildberriesProduct(custom_logger=log, url=url_data).get_data()


def main() -> None:
    """
    Основная функция для запуска обработки данных.
    """

    logger = CustomLogger()
    log = logger.start_initialization()

    # Получение данных о телевизорах
    path_to_csv = Wildberries(custom_logger=log, brand_name=CONFIG_TV['brand_name'], diagonal=CONFIG_TV['diagonal'],
                              price_start=CONFIG_TV['price_start'], price_end=CONFIG_TV['price_end']).get_TV_data()

    # Чтение данных из CSV файла
    all_data = read_csv_without_header(file_path=path_to_csv)

    # Запуск потоков для обработки URL
    threads = []
    for url in all_data:
        if len(threads) >= 5:
            for thread in threads:
                thread.join()
            threads = []
        thread = Thread(target=process_url, args=(url, log))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Обработка PDF файлов
    all_pdf_list = list_files_in_directory(path_to_folder=CONFIG['path_to_save_pdf'])
    for pdf_file in all_pdf_list:
        _pdf = PDF(log=log, path_to_file=pdf_file)
        number_phone, user_email = _pdf.get_data()
        write_data_to_excel_wireBank(data=[number_phone, user_email])


if __name__ == '__main__':
    main()
