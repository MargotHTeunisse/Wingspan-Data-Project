import contextlib
import os
import shutil
import tempfile
import time
from pathlib import Path

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from PIL import Image, ImageChops

from visualization.models import Bird

@contextlib.contextmanager
def make_temp_directory():
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)

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

        #They notice that the search box and search results are aligned.
        searchbox = self.browser.find_element(By.ID,"search")
        search_results = self.browser.find_element(By.ID, "results_list")
        self.assertAlmostEqual(searchbox.location["x"] + searchbox.size["width"]/2,
                               search_results.location["x"] + search_results.size["width"]/2, 0)

        #They notice that the search box is aligned with the selection menu for 1D plotting.
        select_element = self.browser.find_element(By.NAME, "1D_plot_property_selection")
        self.assertAlmostEqual(searchbox.location["y"], select_element.location["y"], -2)

        #They notice that the 1D plotting selection menu is to the right of the search plot.
        self.assertGreater(select_element.location["x"] - select_element.size["width"]/2,
                           searchbox.location["x"] + searchbox.size["width"]/2)

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

        # They wait max. 1 second for the results to load.
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

    def test_can_plot_1d_property_distribution(self):
        # An avid Wingspan player visits the site.
        # They would like to improve their strategy.
        self.browser.get(self.live_server_url)

        with make_temp_directory() as temp_dir_name:
            temp_dir = Path(temp_dir_name)

            # They notice a select menu that allows them to see how the selected property is distributed.
            select_element = self.browser.find_element(By.NAME, "1D_plot_property_selection")
            self.assertIn("Inspect property...", select_element.text)

            # They also notice a blank charting area.
            chart = self.browser.find_element(By.ID, "chart")
            src_blank = str(temp_dir / "blank.png")
            chart.screenshot(src_blank)

            # They want to know how victory points are distributed over birds.
            # They select the 'Victory points' property.
            select = Select(select_element)
            select.select_by_visible_text('Victory points')
            time.sleep(1)

            # Max. 1 second after making their selection, they see a chart appear.
            chart = self.browser.find_element(By.ID, "chart")
            src_victory_points = str(temp_dir / "victory_points.png")
            chart.screenshot(src_victory_points)
            diff = ImageChops.difference(Image.open(src_victory_points),
                                    Image.open(src_blank))
            self.assertIsNotNone(diff.getbbox())

            # Satisfied with the victory points distribution, they also check the distribution of nest capacities.
            #The chart changes visibly.
            select.select_by_visible_text('Nest capacity')
            time.sleep(1)
            chart = self.browser.find_element(By.ID, "chart")
            src_nest_capacity = str(temp_dir / "nest_capacity.png")
            chart.screenshot(src_nest_capacity)
            diff = ImageChops.difference(Image.open(src_nest_capacity),
                                         Image.open(src_blank))
            self.assertIsNotNone(diff.getbbox())
            diff = ImageChops.difference(Image.open(src_nest_capacity),
                                         Image.open(src_victory_points))
            self.assertIsNotNone(diff.getbbox())

        # Satisfied, the user closes the app.
