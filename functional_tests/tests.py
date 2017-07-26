import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        time.sleep(1)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edyta dowiedziałą się o nowej, wspaniałej aplikacji w postaci listy rzeczy do zrobienia
        # Postanowiła więc przejść na stronę głowną tej aplikacji
        self.browser.get(self.live_server_url)

        # Zwrociła uwagę, że tytuł strony i nagłwek zawierający słowo Lisy
        self.assertIn('Listy', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('lista', header_text)

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
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table(row_text='1: Kupić pawie piora')

        # Na stronie nadal znajduje się pole tekstowe zachęcające do podania kolejnego zadania
        # Edyta wpisała "Użyć pawich pior do zrobienia przynęty"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Użyć pawich pior do zrobienia przynęty')
        inputbox.send_keys(Keys.ENTER)

        # Strona została ponownie uaktualniona i teraz wyświetla dwa elementy
        # na liście rzeczy do zrobienia
        self.check_for_row_in_list_table(row_text='1: Kupić pawie piora')
        self.check_for_row_in_list_table(
            row_text='2: Użyć pawich pior do zrobienia przynęty')

        # Teraz nowy użytkownik Franek zaczyna korzystać z witryny

        ## Używa nowej sesji przeglądarki internetowej, aby mieć pewność, że żadne
        ## informacje dotyczące Edyty nie zostaną ujawnione, na przykłąd przez cookies
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