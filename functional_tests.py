from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_wingspan_visualization(self):
        ##Someone visits the website.
        self.browser.get('http://localhost:8000')

        ##They notice that it contains data for the popular board game Wingspan.
        self.assertIn("Wingspan", self.browser.title)

        ##They haven't played the game, but they like birds.
        ##They want to see if their favourite bird, the black-tailed godwit, is in the game.
        ##They look for a search bar.
        searchbox = self.browser.find_element(By.ID, "search")
        self.assertEqual(searchbox.get_attribute("placeholder"), "Look for a bird...")

        ##They would like to use the English name.
        ##They therefore check whether the search bar allows English.
        self.assertNotEqual("EN", searchbox.get_attribute("language"))

        ##Since the language is not set to English, they try the scientific name.
        searchbox.send_keys("Limosa limosa")
        searchbox.send_keys(Keys.ENTER)

        ##They expect only a single result.
        results = self.browser.find_element(By.ID, "search_results")
        self.assertEqual(results.size, 1)

        self.fail("Finish the test!")

        ##Now they want to check that the black-tailed godwit is represented accurately.
        ##They check that the bird:
        ##- lives in wetlands
        ##- nests on the ground
        ##- has a wingspan of 76 cm
        ##- eats bugs and grains, but not berries, fish or rodents.

        ##They notice that it has a nest capacity of 2.
        ##That number doesn't tell them much; they need to see how this compares to other birds.
        ##They plot the nest capacities, and find that 2 is the median nest capacity.

        ##While they make this plot, they still want to keep the black-tailed godwit in view.

        ##They notice that the bird is worth 6 victory points. They wonder what that value is based on.
        ##The black-tailed godwit has 3 food tokens.
        ##Perhaps birds are worth more points the more food they require?
        ##They make a bar chart to check this.

        ##Satisfied, they close the application.





