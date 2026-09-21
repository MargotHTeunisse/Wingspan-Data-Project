import contextlib
import os
import shutil
import tempfile
import time
from pathlib import Path

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from PIL import Image, ImageChops

from visualization.models import Bird

MAX_WAIT = 2

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

    def wait_for_named_search_result(self, name:str):
        start_time = time.time()
        while True:
            try:
                search_results = self.browser.find_elements(By.CLASS_NAME, "search_result")
                self.assertTrue(any([name in result.text for result in search_results]))
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.2)

    def wait_for_chart_change(self, old_img:Image, new_img_src:str):
        start_time = time.time()
        while True:
            try:
                chart = self.browser.find_element(By.ID, "chart")
                chart.screenshot(new_img_src)
                new_img = Image.open(new_img_src).convert('RGB')

                diff = ImageChops.difference(new_img, old_img)
                self.assertIsNotNone(diff.getbbox())
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.2)

    def test_layout_and_styling(self):
        #Someone goes to the home page.
        self.browser.get(self.live_server_url)

        #Their browser windows is set to a specific size.
        self.browser.set_window_size(1024, 768)

        #They notice that the search box and search results are approximately vertically aligned.
        searchbox = self.browser.find_element(By.ID,"search")
        search_results = self.browser.find_element(By.ID, "results_list")
        self.assertAlmostEqual(searchbox.location["x"] + searchbox.size["width"]/2,
                               search_results.location["x"] + search_results.size["width"]/2, -1)

        #They notice that the search and chart areas are precisely horizontally aligned.
        search_area = self.browser.find_element(By.ID, "search_area")
        chart_area = self.browser.find_element(By.ID, "chart_area")
        self.assertEqual(search_area.location["y"], chart_area.location["y"])

        #They notice that the charting and search areas are precisely the same height.
        self.assertEqual(search_area.size["height"], chart_area.size["height"])

        #They notice that the charting area is to the right of the search area.
        self.assertAlmostEqual(chart_area.location["x"],
                           search_area.location["x"] + search_area.size["width"], -1)

    def test_mobile_layout(self):
        #Someone visits to the homepage from a mobile phone.
        #Their screen has a resolution of 375x812 pixels.
        self.browser.set_window_size(375, 812)

        self.browser.get(self.live_server_url)

        #They note that the select menu for the charting area is below the search area.
        search_area = self.browser.find_element(By.ID, "search_area")
        chart_area = self.browser.find_element(By.ID, "chart_area")
        self.assertAlmostEqual(chart_area.location["y"], search_area.location["y"] + search_area.size["height"], -1)

        #They note that the search and charting areas are precisely the same width.
        self.assertEqual(chart_area.size["width"], search_area.size["width"])

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

        # They wait for the results to load.
        self.wait_for_named_search_result("Limosa limosa")

        # They expect to see the black-tailed godwit as the only search result,
        # since they entered the full species name.
        search_results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertEqual(len(search_results), 1)

        # To check that their favourite bird is represented accurately,
        # they check the bird properties.
        # They notice the Dutch name is given, and learn the bird is called 'Grutto'.
        result = search_results[0]
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

        self.wait_for_named_search_result("Falco")

        #They expect all birds to have names starting with the genus 'Falco'.
        search_results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertTrue(all([result.text.startswith("Falco") for result in search_results]))

        # Falcons being common enough, they expect to find at least two.
        self.assertGreater(len(search_results), 1)

        # Satisfied with the game's collection of birds, they close the application.

    def test_can_plot_1d_property_distribution(self):
        # An avid Wingspan player visits the site.
        # They would like to improve their strategy.
        self.browser.get(self.live_server_url)

        #Their browser windows is set to a specific size.
        self.browser.set_window_size(1024, 768)

        with make_temp_directory() as temp_dir_name:
            temp_dir = Path(temp_dir_name)

            # They notice a select menu that allows them to see how the selected property is distributed.
            select_element = self.browser.find_element(By.NAME, "1D_plot_property_selection")
            self.assertIn("Inspect property...", select_element.text)

            # They also notice a blank charting area.
            chart = self.browser.find_element(By.ID, "chart")
            initial_width = chart.size["width"]
            initial_height = chart.size["height"]

            src_blank = str(temp_dir / "blank.png")
            chart.screenshot(src_blank)
            img_blank = Image.open(src_blank).convert('RGB')

            # They want to know how victory points are distributed over birds.
            # They select the 'Victory points' property.
            select = Select(select_element)
            select.select_by_visible_text('Victory points')

            # They wait for the chart to change.
            src_victory_points = str(temp_dir / "victory_points.png")
            self.wait_for_chart_change(img_blank, src_victory_points)
            img_victory_points = Image.open(src_victory_points).convert('RGB')

            # The canvas maintains its size after the chart has changed.
            chart = self.browser.find_element(By.ID, "chart")
            self.assertAlmostEqual(initial_width, chart.size["width"], -1)
            self.assertAlmostEqual(initial_height, chart.size["height"],  -1)


            # Satisfied with the victory points distribution, they also check the distribution of nest capacities.
            select.select_by_visible_text('Nest capacity')

            # They wait again for the chart to change.
            src_nest_capacity = str(temp_dir / "nest_capacity.png")
            self.wait_for_chart_change(img_victory_points, src_nest_capacity)
            img_nest_capacity = Image.open(src_nest_capacity).convert('RGB')

             # The chart having changed, they check that it is not blank.
            diff = ImageChops.difference(img_nest_capacity, img_blank)
            self.assertIsNotNone(diff.getbbox())

        # Satisfied, the user closes the app.
