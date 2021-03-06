import time
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Edyta przeszla na strone glowna
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # Zauwazyla, ze pole tekstowe zostalo elegancko wysrodkowane
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=15
        )

        # Edyta utworzyla nowa liste i zobaczyła
        # że pole tekstowe nadal jest wyśrodkowane
        self.submit_new_item(text='testing')
        time.sleep(1)
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=15
        )
