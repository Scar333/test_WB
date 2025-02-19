import os.path
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Wildberries:
    """Класс для работы с Wildberries"""

    MAIN_URL = 'https://www.wildberries.ru/catalog/elektronika/tv-audio-foto-video-tehnika/televizory/televizory'
    ELEMENT_WAIT_TIME = 10
    WAITING_TIME_ENTER_WORD = 0.3
    CLASSIC_SLEEP_TIME = 5

    def __init__(self, custom_logger: object, brand_name: str, diagonal: str, price_start: str, price_end: str) -> None:
        """
        Инициализация параметров

        :param custom_logger: Объект логгера
        :param brand_name: Название бренда
        :param diagonal: Диагональ экрана
        :param price_start: Начальная цена
        :param price_end: Конечная цена
        """

        self.log = custom_logger
        self.brand_name = brand_name
        self.diagonal = diagonal
        self.price_start = price_start
        self.price_end = price_end
        self._check_price_input_user()

        # Надстройки для браузера
        options = Options()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)

    def _check_price_input_user(self) -> None:
        """Проверка цены, введенной пользователем"""

        if int(self.price_end) < int(self.price_start):
            raise ValueError('Конечная цена должна быть больше начальной цены')

    def scroll_to_element(self, element) -> None:
        """
        Прокрутка страницы к элементу

        :param element: Элемент, к которому нужно прокрутить
        """

        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def smooth_scroll_until_element_appears(self, scroll_pause_time: float = 0.5, scroll_increment: int = 300) -> None:
        """
        Плавно скроллит страницу до тех пор, пока не появится элемент с указанным селектором.

        :param scroll_pause_time: Время паузы между скроллами (в секундах)
        :param scroll_increment: Величина скролла за один шаг (в пикселях)
        """

        max_scrolls = int(20 / scroll_pause_time)  # Максимальное количество попыток скроллинга для 1 минуты
        scroll_count = 0

        while scroll_count < max_scrolls:
            self.driver.execute_script(
                f"window.scrollTo(0, {self.driver.execute_script('return window.scrollY') + scroll_increment});")
            sleep(scroll_pause_time)
            scroll_count += 1

    def _click_check_box(self, element) -> None:
        """
        Нажатие на чекбокс

        :param element: Элемент, содержащий чекбокс
        """

        element.find_element(By.CSS_SELECTOR, '.checkbox-with-text__decor').click()

    def hover_over_element(self, element) -> None:
        """
        Наведение мыши на элемент

        :param element: Элемент, на который нужно навести мышь
        """

        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def _click_all_filters(self) -> None:
        """Нажатие на 'Все фильтры'"""

        self.log.info('Нажимаю "Все фильтры"')

        try:
            all_filters = WebDriverWait(self.driver, timeout=self.ELEMENT_WAIT_TIME).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.dropdown-filter.j-show-all-filtres'))
            )
            all_filters.click()

        except TimeoutException:
            self.log.info(
                f'Не смог найти элемент "Все фильтры" в течение {self.ELEMENT_WAIT_TIME} секунд, завершаю свою работу!')
            raise TimeoutException('Истекло время ожидания появления элемента "Все фильтры"')

        except NoSuchElementException:
            self.log.info('Не смог найти элемент "Все фильтры", завершаю свою работу!')
            raise NoSuchElementException('Не смог найти элемент "Все фильтры"')

        except Exception as ex_all_filters:
            self.log.info(f'Произошла непредвиденная ошибка, завершаю свою работу! Ошибка:\n{ex_all_filters}')
            raise Exception(f'Произошла непредвиденная ошибка, завершаю свою работу!')

    def _check_name_brand(self, name_bran_on_site: str) -> bool:
        """Проверка на совпадение бренда на сайте"""

        return name_bran_on_site.lower() == self.brand_name.lower()

    def _set_brand(self) -> None:
        """Установка бренда"""

        self.log.info('Ввожу название бренда')
        sleep(self.CLASSIC_SLEEP_TIME)
        try:
            # all_brand = WebDriverWait(self.driver, timeout=self.ELEMENT_WAIT_TIME).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR,
            #                                     '.filters-desktop__item.j-filter-container.filters-desktop__item--type-6.filters-desktop__item--fbrand.open.show'))
            # )
            # if all_brand:
            daughter_all_brand = self.driver.find_element(By.CSS_SELECTOR,
                                                          '.filters-desktop__item.j-filter-container.filters-desktop__item--type-6.filters-desktop__item--fbrand.open.show')

            show_all = daughter_all_brand.find_element(By.CSS_SELECTOR, '.filter__show-all.j-show-whole-filters')
            self.scroll_to_element(element=daughter_all_brand)
            daughter_all_brand.click()
            sleep(self.CLASSIC_SLEEP_TIME)

            show_all.click()
            sleep(self.CLASSIC_SLEEP_TIME)

            brand_input = daughter_all_brand.find_element(By.CSS_SELECTOR, '.j-search-filter')
            brand_input.clear()
            for char in self.brand_name:
                brand_input.send_keys(char)
                sleep(self.WAITING_TIME_ENTER_WORD)

            name_bran_on_site = daughter_all_brand.find_element(By.CSS_SELECTOR, '.filter__list').text.split('\n')[
                0]
            if self._check_name_brand(name_bran_on_site):
                self.log.info(f'Бренд "{self.brand_name}" существует, выбираю его!')
                self._click_check_box(element=daughter_all_brand)
                sleep(self.CLASSIC_SLEEP_TIME)

            else:
                self.log.info(
                    f'Бренда "{self.brand_name}" не существует, проверьте корректность ввода бренда! Первый попавшийся бренд, это: {name_bran_on_site}')
                raise ValueError(f'Бренда "{self.brand_name}" не существует, проверьте корректность ввода бренда!')

            # else:
            #     self.log.info(f'Не смог найти "Бренды"')
            #     raise ValueError(f'Бренда "{self.brand_name}" не существует, проверьте корректность ввода бренда!')

        except NoSuchElementException:
            self.log.info('Не смог найти окно "Бренд", завершаю свою работу!')
            raise NoSuchElementException('Не смог найти элемент "Бренд"')

        except Exception as ex_all_filters:
            self.log.info(f'Произошла непредвиденная ошибка, завершаю свою работу! Ошибка:\n{ex_all_filters}')
            raise Exception(f'Произошла непредвиденная ошибка, завершаю свою работу!')

    def _set_diagonal(self) -> None:
        """Установка диагонали"""

        self.log.info('Выбираю диагональ')

        try:
            all_diagonal = self.driver.find_element(By.CSS_SELECTOR,
                                                    '.filters-desktop__item.j-filter-container.filters-desktop__item--type-1.filters-desktop__item--f92740.open.show')
            self.scroll_to_element(element=all_diagonal)
            sleep(self.CLASSIC_SLEEP_TIME)

        except NoSuchElementException:
            self.log.info('Не смог найти окно "Диагональ", завершаю свою работу!')
            raise NoSuchElementException('Не смог найти элемент "Диагональ"')

        try:
            diagonals = all_diagonal.find_element(By.CSS_SELECTOR, '.filter__list')
            all_diagonals = diagonals.find_elements(By.CSS_SELECTOR, '.filter__item')
            for diagonal in all_diagonals:
                if diagonal.text[0:2] == self.diagonal:
                    self._click_check_box(element=diagonal)
                    break

            else:
                self.log.info(
                    f'Не смог найти диагональ "{self.diagonal}" у бренда {self.brand_name}! Продолжаю работу без нее!')

        except Exception as ex_diagonal:
            self.log.info(f'Произошла непредвиденная ошибка! Ошибка:\n{ex_diagonal}')
            raise Exception(f'Произошла непредвиденная ошибка, завершаю свою работу!')

    def _click_button_view(self) -> None:
        """Нажатие на кнопку 'Показать'"""

        self.log.info('Применяю фильтры')

        try:
            self.driver.find_element(By.CSS_SELECTOR, '.filters-desktop__btn-main.btn-main').click()
            sleep(self.WAITING_TIME_ENTER_WORD)

        except NoSuchElementException:
            self.log.info('Не смог найти кнопку "Показать", завершаю свою работу!')
            raise NoSuchElementException('Не смог найти кнопку "Показать"')

        except Exception as ex_button_view:
            self.log.info(
                f'Произошла непредвиденная ошибка при применении фильтров, завершаю свою работу! Ошибка:\n{ex_button_view}')

            raise Exception('Произошла непредвиденная ошибка!')

    def _set_price(self) -> None:
        """Проставление цены"""

        self.log.info('Проставляю цену')

        try:
            elem_price = self.driver.find_element(By.CSS_SELECTOR, '.dropdown-filter__btn.dropdown-filter__btn--priceU')
            self.hover_over_element(element=elem_price)

        except NoSuchElementException:
            pass

        try:
            elem_price_start = self.driver.find_element(By.CSS_SELECTOR, 'input.j-price[name="startN"]')
            elem_price_start.click()
            elem_price_start.clear()
            for char in self.price_start:
                elem_price_start.send_keys(char)
                sleep(self.WAITING_TIME_ENTER_WORD)


            elem_price_end = self.driver.find_element(By.CSS_SELECTOR, 'input.j-price[name="endN"]')
            elem_price_end.click()
            elem_price_end.clear()
            for char in self.price_end:
                elem_price_end.send_keys(char)
                sleep(self.WAITING_TIME_ENTER_WORD)

            sleep(self.WAITING_TIME_ENTER_WORD)

            if 'Не нашлось подходящих товаров'.lower() in self.driver.find_element(By.CSS_SELECTOR,
                                                                                   '.not-found-result').text.lower():
                self.log.info('Нет результатов с такой ценой!')
                raise Exception('Нет результатов с такой ценой!')

        except Exception as ex:
            self.log.info(f'Произошла ошибка при установке цены: {ex}')
            raise Exception('Произошла ошибка при установке цены!')

    def _all_product(self) -> str | None:
        """Сбор всех ссылок на товары"""

        path_to_csv = os.path.join(os.getcwd(), 'urls.csv')

        while True:
            try:
                self.smooth_scroll_until_element_appears()
                product_cards = self.driver.find_elements(By.CSS_SELECTOR, 'article.product-card')
                product_links = [card.find_element(By.CSS_SELECTOR, 'a.j-card-link').get_attribute('href') for card in
                                 product_cards]

                with open(path_to_csv, 'a', encoding='utf-8') as file:
                    for url in product_links:
                        file.write(url + '\n')

                next_page = self.driver.find_element(By.CSS_SELECTOR, '.pagination-next.pagination__next.j-next-page')
                self.scroll_to_element(element=product_cards[-1])
                next_page.click()


            except NoSuchElementException:
                break

        self.driver.close()
        self.driver.quit()
        return path_to_csv

    def get_TV_data(self) -> str | None:
        """Основной метод для получения данных о телевизорах"""

        self.driver.get(self.MAIN_URL)
        self._click_all_filters()
        self._set_price()
        self._set_brand()
        self._set_diagonal()
        self._click_button_view()
        return self._all_product()
