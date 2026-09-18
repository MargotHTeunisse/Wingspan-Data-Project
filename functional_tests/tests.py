import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from visualization.models import Bird


class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        opts = webdriver.FirefoxOptions()
        opts.add_argument("--headless")
        self.browser = webdriver.Firefox(options=opts)

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

    def test_can_look_up_birds(self):
        # Setup for test database
        bird = Bird()
        bird.scientific_name = "Limosa limosa"
        bird.nl_name = "Grutto"
        bird.nest_capacity = 2
        bird.wingspan = 76
        bird.worms = 1
        bird.grains = 1
        bird.save()

        bird = Bird()
        bird.scientific_name = "Falco peregrinus"
        bird.save()

        bird = Bird()
        bird.scientific_name = "Falco subbuteo"
        bird.save()

        ##Someone visits the website.
        self.browser.get(self.live_server_url)

        ##They notice that it contains data for the popular board game Wingspan.
        self.assertIn("Wingspan", self.browser.title)

        ##They haven't played the game, but they know it's about birds.
        ##They see a search bar; the search results are empty.
        searchbox = self.browser.find_element(By.ID, "search")
        results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertEqual(0, len(results))
        # The search bar asks for the scientific name.
        self.assertEqual("Enter scientific name...", searchbox.get_attribute("placeholder"))

        ##They first look up their favourite bird, the black-tailed godwit.
        ##The user knows the scientific name of the black-tailed godwit is 'Limosa limosa'.
        searchbox.send_keys("Limosa limosa")
        searchbox.send_keys(Keys.ENTER)

        # They wait max. 5 seconds for the results to load.
        time.sleep(1)

        # They expect to see the black-tailed godwit as the only search result,
        # since they entered the full species name.
        search_results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertEqual(len(search_results), 1)
        result = search_results[0]
        self.assertIn("Limosa limosa", result.text)

        # To check that their favourite bird is represented accurately,
        # they check the bird properties.
        # They notice the Dutch name is given, and learn the bird is called 'Grutto'.
        self.assertIn("🇳🇱 Grutto", result.text)

        # They see that the black-tailed godwit:
        # - has a nest capacity of 2
        # - has a wingspan of 76cm
        # - eats bugs and grains, but not berries, fish or rodents.
        self.assertIn("76cm", result.text)
        self.assertTrue(result.text.count("🥚") == 2)
        self.assertIn("🌾", result.text)
        self.assertIn("🐛", result.text)
        self.assertNotIn("🐟", result.text)
        self.assertNotIn("🐁", result.text)
        self.assertNotIn("🍒", result.text)

        # Reassured that their favourite bird is in the game, the user is curious to see other birds.
        # They enter the 'Falco' genus to find out how many falcons the game contains.
        searchbox = self.browser.find_element(By.ID, "search")
        searchbox.send_keys("falco")
        searchbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # Falcons being common enough, they expect to find at least two.
        search_results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertGreater(len(search_results), 1)
        self.assertTrue(all([result.text.startswith("Falco") for result in search_results]))

        # Satisfied with the game's collection of birds, they close the application.