from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edyta przeszła na stronę główną i przypadkowo spróbowała utworzyć
        # pusty element na liście. Nacisnęła klawisz Enter w pusty polu
        # tekstowym
        self.browser.get(self.live_server_url)
        self.submit_new_item(text='')

        # po odświeżeniu strony głównej zobaczyła komunikat błędu
        # infomrujący o niemożliwości utworzenia pustego elementu na liście
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Element nie może być pusty")

        # Spróbowała ponownie, wpisując dowolny tekst i wszystko zadziałało
        self.submit_new_item(text='Kupić mleko')
        self.wait_for_row_in_list_table(row_text='1: Kupić mleko')

        # Przekornie po raz drugi spróbowała utworzyć pusty element na liście
        self.submit_new_item(text='')

        # Na stronie listy otrzymałą ostrzeżenie podobne do wcześniejszego
        self.wait_for_row_in_list_table(row_text='1: Kupić mleko')
        error = self.browser.find_element_by_css_selector('.has-error')
        self.assertEqual(error.text, "Element nie może być pusty")
        
        # Element mogła poprawić, wpisując w nim dowolny tekst
        self.submit_new_item(text='Zrobić herbatę')
        self.wait_for_row_in_list_table(row_text='1: Kupić mleko')
        self.wait_for_row_in_list_table(row_text='2: Zrobić herbatę')