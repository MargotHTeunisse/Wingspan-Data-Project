from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_layout_and_styling(self):
        #Someone goes to the home page.
        self.browser.get('http://localhost:8000')

        #Their browser windows is set to a specific size.
        self.browser.set_window_size(1024, 768)

        #They notice the search box is centered.
        searchbox = self.browser.find_element(By.ID,"search")
        self.assertAlmostEqual(searchbox.location["x"] + searchbox.size["width"]/2,
                               512, delta=10)

        #They notice the results are centered as well.
        searchbox = self.browser.find_element(By.ID, "results_table")
        self.assertAlmostEqual(searchbox.location["x"] + searchbox.size["width"] / 2,
                               512, delta=10)

    def test_can_look_up_bird(self):
        ##Someone visits the website.
        self.browser.get('http://localhost:8000')

        ##They notice that it contains data for the popular board game Wingspan.
        self.assertIn("Wingspan", self.browser.title)

        ##They haven't played the game, but they know it's about birds.
        ##They want to look up their favourite bird, the black-tailed godwit.

        ##They see a search bar; the search results are empty.
        searchbox = self.browser.find_element(By.ID, "search")
        results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertEqual(0, len(results))
        #The search bar asks for the scientific name.
        self.assertEqual("Enter scientific name...", searchbox.get_attribute("placeholder"))

        ##They know the scientific name is 'Limosa limosa'.
        ##They assume 'Limosa' should narrow it down enough.
        searchbox.send_keys("Limosa")
        searchbox.send_keys(Keys.ENTER)

        #They wait max. 1 seconds for the results to load.
        time.sleep(1)

        #They expect to find 'Limosa limosa' among the search results.
        search_results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertGreater(len(search_results), 0)
        self.assertTrue(any([result.text == "Limosa limosa" for  result in search_results]))

        self.fail("Finish the test!")

        ##Now they want to check that the black-tailed godwit is represented accurately.
        ##They check that the bird:
        ##- lives in wetlands
        ##- nests on the ground
        ##- has a wingspan of 76 cm
        ##- eats bugs and grains, but not berries, fish or rodents.

        ##Satisfied, they close the application.





