from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By

class LayoutTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_layout_and_styling(self):
        #Someone goes to the home page.
        self.browser.get(self.live_server_url)

        #Their browser windows is set to a specific size.
        self.browser.set_window_size(1024, 768)

        #They notice the search box is centered.
        searchbox = self.browser.find_element(By.ID,"search")
        self.assertAlmostEqual(searchbox.location["x"] + searchbox.size["width"]/2,
                               512, delta=10)

        #They notice the results are centered as well.
        searchbox = self.browser.find_element(By.ID, "results_list")
        self.assertAlmostEqual(searchbox.location["x"] + searchbox.size["width"] / 2,
                               512, delta=10)