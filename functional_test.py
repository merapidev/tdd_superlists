import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        self.browser.implicitly_wait(1)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edyta dowiedziałą się o nowej, wspaniałej aplikacji w postaci listy rzeczy do zrobienia
        # Postanowiła więc przejść na stronę głowną tej aplikacji
        self.browser.get('http://localhost:8000')

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

        # Edyta była ciekawa, czy witryna zapamięta jej listę. Zwrociła uwagę na wygnerowany dla niej
        # unikatowy adres URL, obok ktorego znajduej się pewien tekst z
        # wyjaśnieniem
        self.fail('Zakonczenie testu!')

        # Przechodzi pod podany adres URL i widzi wyświetloną swoją listę
        # rzeczy do zrobienia

        # Usatysfakcjonowana kładzie się spać

if __name__ == '__main__':
    unittest.main()
