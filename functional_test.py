import unittest
from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edyta dowiedziałą się o nowej, wspaniałej aplikacji w postaci listy rzeczy do zrobienia
        # Postanowiła więc przejść na stronę głowną tej aplikacji
        self.browser.get('http://localhost:8000')

        # Zwrociła uwagę, że tytuł strony i nagłwek zawierający słowo Lisy
        self.assertIn('Listy', self.browser.title)
        self.fail('Zakonczenie testu!')

        # Od razu zostaje zachęconam aby wpisać rzecz do zrobienia

        # W polu tekstowym wspiała "Kupić pawie piora"

        # Po naciśnięciu klawisza Enter strona została zaktualizowana i wyświetla 
        # "1: Kupić pawie piora" jako element listy rzeczy do zrobienia

        # Na stronie nadal znajduje się pole tekstowe zachęcające do podania kolejnego zadania
        # Edyta wpisała "Użyć pawich pior do zrobienia przynęty"

        # Strona została ponownie uaktualniona i teraz wyświetla dwa elementy na liście rzeczy do zrobienia

        # Edyta była ciekawa, czy witryna zapamięta jej listę. Zwrociła uwagę na wygnerowany dla niej 
        # unikatowy adres URL, obok ktorego znajduej się pewien tekst z wyjaśnieniem

        # Przechodzi pod podany adres URL i widzi wyświetloną swoją listę rzeczy do zrobienia

        # Usatysfakcjonowana kładzie się spać

if __name__ == '__main__':
    unittest.main()