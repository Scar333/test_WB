import os.path
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from other import create_folder
from config import CONFIG


class WildberriesProduct:
    """Класс для работы с товарами на Wildberries"""

    PATH_TO_SAVE_FILE = CONFIG['path_to_save_pdf']
    ELEMENT_WAIT_TIME = 10
    WAITING_TIME_ENTER_WORD = 0.3
    CLASSIC_SLEEP_TIME = 5

    def __init__(self, custom_logger: object, url: str) -> None:
        """
        Инициализация параметров

        :param custom_logger: Объект логгера
        :param url: URL страницы продукта
        """

        self.log = custom_logger
        self.url = url

        create_folder(self.PATH_TO_SAVE_FILE)

        # Надстройки для браузера
        options = Options()
        options.add_argument("--start-maximized")
        options.add_experimental_option("prefs", {
            "download.default_directory": self.PATH_TO_SAVE_FILE,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        self.driver = webdriver.Chrome(options=options)

    def _go_to_product_page(self) -> None:
        """Переход на страницу товара"""

        self.driver.get(self.url)

    def _waiting_elem(self) -> None:
        """Ожидание элемента 'Все характеристики и описание' и клик по нему"""

        try:
            all_filters = WebDriverWait(self.driver, timeout=self.ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.product-page__btn-detail.hide-mobile.j-details-btn-desktop'))
            )
            all_filters.click()
            sleep(self.CLASSIC_SLEEP_TIME)

        except TimeoutException:
            self.log.info(
                f'Не смог найти элемент "Все характеристики и описание" в течение {self.ELEMENT_WAIT_TIME} секунд, завершаю свою работу!')
            raise TimeoutException('Истекло время ожидания появления элемента "Все характеристики и описание"')

        except NoSuchElementException:
            self.log.info('Не смог найти элемент "Все характеристики и описание", завершаю свою работу!')
            raise NoSuchElementException('Не смог найти элемент "Все характеристики и описание"')

        except Exception as ex_all_filters:
            self.log.info(f'Произошла непредвиденная ошибка, завершаю свою работу! Ошибка:\n{ex_all_filters}')
            raise Exception(f'Произошла непредвиденная ошибка, завершаю свою работу!')

    def _check_doc(self) -> bool:
        """Проверка наличия кнопки 'Документы проверены' и клик по ней"""

        try:
            doc_check = self.driver.find_element(By.CSS_SELECTOR, '.btn-certificate')
            doc_check.click()
            sleep(self.CLASSIC_SLEEP_TIME)
            self.driver.find_element(By.CSS_SELECTOR, '.popup__step-link').click()
            sleep(self.CLASSIC_SLEEP_TIME)
            return True

        except NoSuchElementException:
            self.log.info('Не смог найти элемент "Документы проверены", завершаю свою работу!')
            return False

    def _download_doc(self) -> None:
        """Скачивание документа"""

        try:
            self.driver.switch_to.window(self.driver.window_handles[1])
            down_button = WebDriverWait(self.driver, timeout=self.ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.btn.btn_accent.btn-download-pdf'))
            )
            sleep(self.CLASSIC_SLEEP_TIME)
            down_button.click()
            sleep(self.CLASSIC_SLEEP_TIME)

        except Exception as ex:
            self.log.info(f'Произошла ошибка при скачивании документа: {ex}')

    def get_data(self) -> None:
        """Основной метод для получения данных о товаре"""

        self._go_to_product_page()
        self._waiting_elem()
        if self._check_doc():
            self._download_doc()
        self.driver.close()
        self.driver.quit()
