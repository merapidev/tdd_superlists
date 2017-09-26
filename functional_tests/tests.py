import time
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as exc:
                if time.time() - start_time > MAX_WAIT:
                    raise exc
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edyta dowiedziałą się o nowej, wspaniałej aplikacji w postaci listy rzeczy do zrobienia
        # Postanowiła więc przejść na stronę głowną tej aplikacji
        self.browser.get(self.live_server_url)

        # Zwrociła uwagę, że tytuł strony i nagłwek zawierający słowo Lisy
        self.assertIn('Listy', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('listę', header_text)

        # Od razu zostaje zachęconam aby wpisać rzecz do zrobienia
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            'Wpisz rzecz do zrobienia',
            inputbox.get_attribute('placeholder')
        )

        # W polu tekstowym wspiała "Kupić pawie piora"
        inputbox.send_keys('Kupić pawie piora')

        # Po naciśnięciu klawisza Enter strona została zaktualizowana i wyświetla
        # "1: Kupić pawie piora" jako element listy rzeczy do zrobienia
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.wait_for_row_in_list_table(row_text='1: Kupić pawie piora')

        # Na stronie nadal znajduje się pole tekstowe zachęcające do podania kolejnego zadania
        # Edyta wpisała "Użyć pawich pior do zrobienia przynęty"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Użyć pawich pior do zrobienia przynęty')
        inputbox.send_keys(Keys.ENTER)

        # Strona została ponownie uaktualniona i teraz wyświetla dwa elementy
        # na liście rzeczy do zrobienia
        self.wait_for_row_in_list_table(row_text='1: Kupić pawie piora')
        self.wait_for_row_in_list_table(
            row_text='2: Użyć pawich pior do zrobienia przynęty')

        # Teraz nowy użytkownik Franek zaczyna korzystać z witryny

        # Używa nowej sesji przeglądarki internetowej, aby mieć pewność, że żadne
        # informacje dotyczące Edyty nie zostaną ujawnione, na przykłąd przez
        # cookies
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Franek odwiedza stronę głowną
        # Nie znajduje żadnych śladow listy Edyty
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kupić pawie piora', page_text)
        self.assertNotIn('zrobienia przynęty', page_text)

        # Franek tworzy nową listę, wprowadzając nowy element
        # Jego lista jest mniej interesująca niż Edyty...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Kupić mleko')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Franek otrzymuje unikatowy adres URL prowadzący do listy
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Ponownie nie ma żadnego śladu po liście Edyty
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kupić pawie piora', page_text)
        self.assertIn('Kupić mleko', page_text)

        # Usatysfakcjonowana kładzie się spać
        self.fail('Zakonczenie testu!')

    def test_layout_and_styling(self):
        # Edyta przeszla na strone glowna
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Zauwazyla, ze pole tekstowe zostalo elegancko wysrodkowane
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=15
        )

        # Edyta utworzyla nowa liste i zobaczyła
        # że pole tekstowe nadal jest wyśrodkowane
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=15
        )
