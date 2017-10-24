import time
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

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
        self.submit_new_item(text='Użyć pawich pior do zrobienia przynęty')

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
        self.submit_new_item(text='Kupić mleko')
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
