import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from visualization.models import Bird


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        for scientific_name in ["Limosa limosa", "Falco peregrinus", "Falco subbutea"]:
            bird = Bird()
            bird.scientific_name = scientific_name
            bird.save()

        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_look_up_birds(self):
        ##Someone visits the website.
        self.browser.get(self.live_server_url)

        ##They notice that it contains data for the popular board game Wingspan.
        self.assertIn("Wingspan", self.browser.title)

        ##They haven't played the game, but they know it's about birds.
        ##They see a search bar; the search results are empty.
        searchbox = self.browser.find_element(By.ID, "search")
        results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertEqual(0, len(results))
        #The search bar asks for the scientific name.
        self.assertEqual("Enter scientific name...", searchbox.get_attribute("placeholder"))

        ##They first look up their favourite bird, the black-tailed godwit.
        ##The user knows the scientific name of the black-tailed godwit is 'Limosa limosa'.
        searchbox.send_keys("Limosa limosa")
        searchbox.send_keys(Keys.ENTER)

        #They wait max. 1 seconds for the results to load.
        time.sleep(1)

        #They expect to see the black-tailed godwit as the only search result,
        # since they entered the full species name.
        search_results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertEqual(len(search_results), 1)
        self.assertTrue(any([result.text == "Limosa limosa" for  result in search_results]))

        #Reassured that their favourite bird is in the game, the user is curious to see other birds.
        #They enter the 'Falco' genus to find out how many falcons the game contains.
        searchbox = self.browser.find_element(By.ID, "search")
        searchbox.send_keys("Falco")
        searchbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #Falcons being common enough, they expect to find at least two.
        search_results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertGreater(len(search_results), 1)
        self.assertTrue(all([result.text.startswith("Falco") for  result in search_results]))

        #Satisfied with the game's collection of birds, they close the application.





