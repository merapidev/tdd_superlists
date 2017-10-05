import time
from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):

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
