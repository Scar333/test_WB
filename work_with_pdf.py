import fitz


class PDF:
    """Класс для работы с PDF"""

    def __init__(self, log: object, path_to_file: str) -> None:
        """
        Инициализация параметров

        :param path_to_file: Полный путь до PDF файла
        """

        self.log = log
        self.path_to_file = path_to_file
        self.text = self._get_text_pdf()

    def _get_text_pdf(self) -> list | None:
        """Получение текста из PDF документа"""

        pdf_text = ''

        try:
            with fitz.open(self.path_to_file) as doc:
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    pdf_text += page.get_text()

        except Exception as ex_read_pdf:
            self.log.info(f'Произошла непредвиденная ошибка при чтении PDF файла! Ошибка:\n{ex_read_pdf}')

            return None

        return pdf_text.split('\n')

    def _find_value_by_key(self, key) -> str | None:
        """Находит значение по ключу в тексте"""

        for idx, data in enumerate(self.text):
            if data.lower() == key.lower():
                return self.text[idx + 1]

        return None

    def _get_number(self) -> str | None:
        """Получение номера телефона"""

        return self._find_value_by_key('номер телефона')

    def _get_email(self) -> str | None:
        """Получение email"""

        return self._find_value_by_key('адрес электронной почты')

    def get_data(self) -> tuple | None:
        """Получение данных из PDF"""

        if self.text:
            number_phone = self._get_number()
            user_email = self._get_email()

            return number_phone, user_email

        else:
            self.log.info('Не смог получить данные из PDF файла!')

            return None, None
