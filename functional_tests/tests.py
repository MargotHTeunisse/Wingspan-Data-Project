import contextlib
import shutil
import tempfile
import time
from pathlib import Path

from PIL import Image, ImageChops
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from visualization.models import Bird

MAX_WAIT = 2
ANIMATION_DURATION = 0.5

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

        # Setup for test database
        bird = Bird()
        bird.scientific_name = "Limosa limosa"
        bird.nl_name = "Grutto"
        bird.nest_capacity = 2
        bird.wingspan = 76
        bird.worms = 1
        bird.grains = 1
        bird.lives_in_wetlands = True
        bird.victory_points = 6
        bird.save()

        bird = Bird()
        bird.scientific_name = "Falco peregrinus"
        bird.lives_in_grasslands = True
        bird.lives_in_wetlands = True
        bird.victory_points = 5
        bird.save()

        bird = Bird()
        bird.scientific_name = "Falco subbuteo"
        bird.lives_in_forest = True
        bird.lives_in_grasslands = True
        bird.lives_in_wetlands = True
        bird.victory_points = 4
        bird.save()

        bird = Bird()
        bird.scientific_name = "Accipiter gentilis"
        bird.lives_in_forest = True
        bird.victory_points = 5
        bird.save()

    def tearDown(self):
        self.browser.quit()

    @staticmethod
    def wait_for(assertion):
        start_time = time.time()
        while True:
            try:
                assertion()
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.2)

    def assert_chart_changed(self, old_img:Image, new_img_src:str):
        chart = self.browser.find_element(By.ID, "chart")
        chart.screenshot(new_img_src)
        new_img = Image.open(new_img_src).convert('RGB')

        diff = ImageChops.difference(new_img, old_img)
        self.assertIsNotNone(diff.getbbox())

        # Wait a set time for animation to load
        time.sleep(ANIMATION_DURATION)
        chart.screenshot(new_img_src)

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
        self.wait_for(
             lambda: self.assertEqual(1, len(self.browser.find_elements(By.CLASS_NAME, "search_result")))
        )

        # They expect to see the black-tailed godwit as the only search result.
        search_results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertIn("Limosa limosa", search_results[0].text)

        # To check that their favourite bird is represented accurately,
        # they check the bird properties.
        # They notice the Dutch name is given, and learn the bird is called 'Grutto'.
        result = search_results[0]
        self.assertIn("🇳🇱 Grutto", result.text)

        # They see that the black-tailed godwit:
        # - lives in wetlands
        # - has a nest capacity of 2
        # - has a wingspan of 76cm
        # - eats bugs and grains, but not berries, fish or rodents.
        self.assertIn("💧", result.text)
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

        self.wait_for(lambda:   self.assertTrue(any(["Falco" in result.text for result
                             in self.browser.find_elements(By.CLASS_NAME, "search_result")])))

        #They expect all birds to have 'Falco' in their name.
        search_results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertTrue(all(["Falco" in result.text for result in search_results]))

        # Falcons being common enough, they expect to find at least two.
        self.assertGreater(len(search_results), 1)

        # Satisfied with the game's collection of birds, they close the application.

    def test_can_filter_search_by_bird_properties(self):
        # A Wingspan player visits the site.
        # They want to look up certain bird cards.
        self.browser.get(self.live_server_url)

        # They notice a search form.
        search_form = self.browser.find_element(By.ID, "search_form")

        # Bird names don't mean much to them; they rather want to search by bird properties.
        # The search form has a filter function.
        # They notice the filter contains at least three check boxes.
        check_boxes = search_form.find_elements(By.XPATH, "//input[@type='checkbox']")
        self.assertGreater(len(check_boxes), 2)

        # These three check boxes are associated with the bird habitats: forest, grasslands and wetlands.
        check_box_labels = [label.text for label in
                            search_form.find_elements(By.XPATH, "//input[@type='checkbox']/parent::label")]

        self.assertIn('Forest', check_box_labels)
        self.assertIn('Grasslands', check_box_labels)
        self.assertIn('Wetlands', check_box_labels)

        # They are interested in forest birds, so they click this box.
        forest_checkbox = search_form.find_element(By.NAME, "forest")
        forest_checkbox.click()

        # They make a search request, leaving the search field empty.
        searchbox = search_form.find_element(By.ID, "search")
        searchbox.send_keys(Keys.ENTER)

        # After the results load, they see two birds:
        # the Eurasian hobby and the Northern goshawk.
        self.wait_for(lambda: self.assertTrue(any(["Falco subbuteo" in result.text for result
                             in self.browser.find_elements(By.CLASS_NAME, "search_result")])))

        search_results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertEqual(len(search_results), 2)
        self.assertTrue(any(["Accipiter gentilis" in result.text for result in search_results]))

        # They now try the grasslands filter.
        # This gives them the two falcons.
        grasslands_checkbox = self.browser.find_element(By.NAME, "grasslands")
        grasslands_checkbox.click()
        searchbox = self.browser.find_element(By.ID, "search")
        searchbox.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(any(["Falco peregrinus" in result.text for result
                             in self.browser.find_elements(By.CLASS_NAME, "search_result")])))

        search_results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertEqual(len(search_results), 2)

        # Finally, they click the wetlands filter.
        # This gives them the two falcons and the black-tailed godwit,
        # but not the goshawk.
        wetlands_checkbox = self.browser.find_element(By.NAME, "wetlands")
        wetlands_checkbox.click()

        searchbox = self.browser.find_element(By.ID, "search")
        searchbox.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(any(["Limosa limosa" in result.text for result
                             in self.browser.find_elements(By.CLASS_NAME, "search_result")])))

        search_results = self.browser.find_elements(By.CLASS_NAME, "search_result")
        self.assertEqual(len(search_results), 3)
        self.assertNotIn("Accipiter gentilis", [result.text for result in search_results])

        # Satisfied, the user closes the app.

    def test_can_plot_1d_property_distribution(self):
        # An avid Wingspan player visits the site.
        # They would like to improve their strategy.
        self.browser.get(self.live_server_url)

        #Their browser windows is set to a specific size.
        self.browser.set_window_size(1024, 768)

        with make_temp_directory() as temp_dir_name:
            temp_dir = Path(temp_dir_name)

            # They notice a select menu.
            select_element = self.browser.find_element(By.TAG_NAME, "select")

            # They also notice a blank charting area.
            chart = self.browser.find_element(By.ID, "chart")
            initial_width = chart.size["width"]
            initial_height = chart.size["height"]

            src_blank = str(temp_dir / "blank.png")
            chart.screenshot(src_blank)
            img_blank = Image.open(src_blank).convert('RGB')

            # They want to know how victory points are distributed over birds.
            # They select the 'Victory points' property and click the 'Plot' button.
            select = Select(select_element)
            select.select_by_visible_text('Victory points')
            plot_button = self.browser.find_element(By.XPATH, "//input[@type='button' and @value='Plot']")
            plot_button.click()

            # They wait for the chart to change.
            src_victory_points = str(temp_dir / "victory_points.png")
            self.wait_for(lambda: self.assert_chart_changed(img_blank, src_victory_points))
            img_victory_points = Image.open(src_victory_points).convert('RGB')

            # The canvas maintains its size after the chart has changed.
            chart = self.browser.find_element(By.ID, "chart")
            self.assertAlmostEqual(initial_width, chart.size["width"], -1)
            self.assertAlmostEqual(initial_height, chart.size["height"],  -1)


            # Satisfied with the victory points distribution, they also check the distribution of nest capacities.
            select.select_by_visible_text('Nest capacity')
            plot_button.click()

            # They wait again for the chart to change.
            src_nest_capacity = str(temp_dir / "nest_capacity.png")
            self.wait_for(lambda:self.assert_chart_changed(img_victory_points, src_nest_capacity))
            img_nest_capacity = Image.open(src_nest_capacity).convert('RGB')

             # The chart having changed, they check that it is not blank.
            diff = ImageChops.difference(img_nest_capacity, img_blank)
            self.assertIsNotNone(diff.getbbox())

        # Satisfied, the user closes the app.

    def test_can_plot_in_search_only_mode(self):
        # An avid Wingspan player visits the website.
        # They want to improve their forest engine,
        # and are therefore interested in the property distribution of forest birds.
        self.browser.get(self.live_server_url)

        with make_temp_directory() as temp_dir_name:
            temp_dir = Path(temp_dir_name)

            # They notice a blank charting area.
            chart = self.browser.find_element(By.ID, "chart")
            src_blank = str(temp_dir / "blank.png")
            chart.screenshot(src_blank)
            img_blank = Image.open(src_blank).convert('RGB')

            # They see a toggle to only plot search results.
            # This is what they are looking for, but the toggle is currently disabled,
            # since they have not made a search yet.
            search_only_toggle = self.browser.find_element(By.XPATH,
                                                       "//input[@type='checkbox' and @id='search_only']")
            self.assertTrue(search_only_toggle.get_attribute('disabled'))

            # They try to make an empty search, and find they can now toggle search-only mode.
            searchbox = self.browser.find_element(By.ID, "search")
            searchbox.send_keys(Keys.ENTER)

            self.wait_for(lambda: self.assertFalse(self.browser.find_element(By.XPATH,
                                                       "//input[@type='checkbox' and @id='search_only']")
                                               .get_attribute('disabled')))

            # They request a victory points plot, and wait for the chart to change.
            select_element = self.browser.find_element(By.TAG_NAME, "select")
            select = Select(select_element)
            select.select_by_visible_text('Victory points')
            plot_button = self.browser.find_element(By.XPATH, "//input[@type='button' and @value='Plot']")
            plot_button.click()

            src_victory_points = str(temp_dir/ "victory_points.png")
            self.wait_for(lambda: self.assert_chart_changed(img_blank, src_victory_points))
            img_victory_points = Image.open(src_victory_points).convert('RGB')

            # Comparing the two modes,
            # they find that search-only mode does not change the plot,
            # because they have not filtered out any birds.
            search_only_toggle = self.browser.find_element(By.XPATH,
                                                           "//input[@type='checkbox' and @id='search_only']")
            search_only_toggle.click()
            plot_button.click()

            src_victory_points_search_only = str(temp_dir / "victory_points_search_only.png")
            self.wait_for(lambda: self.assert_chart_changed(img_victory_points, src_victory_points_search_only))
            img_victory_points_search_only = Image.open(src_victory_points_search_only).convert('RGB')

            diff = ImageChops.difference(img_victory_points_search_only, img_victory_points)
            self.assertIsNone(diff.getbbox())

            # They make a search again, this time toggling the filter for the forest habitat.
            forest_checkbox = self.browser.find_element(By.NAME, "forest")
            forest_checkbox.click()

            searchbox = self.browser.find_element(By.ID, "search")
            searchbox.send_keys(Keys.ENTER)

            # They wait until they see the non-forest birds disappear from the search results,
            # then make another plot in search-only mode.
            self.wait_for(lambda: self.assertTrue(any(["Limosa limosa" not in result.text for result
                                                       in self.browser.find_elements(By.CLASS_NAME, "search_result")])))

            plot_button = self.browser.find_element(By.XPATH, "//input[@type='button' and @value='Plot']")
            search_only_toggle = self.browser.find_element(By.XPATH,
                                                           "//input[@type='checkbox' and @id='search_only']")
            search_only_toggle.click()
            plot_button.click()

            # They now see that the plot has changed.
            src_victory_points_search_only = str(temp_dir / "victory_points_search_only.png")
            self.wait_for(lambda: self.assert_chart_changed(img_victory_points, src_victory_points_search_only))
            img_victory_points_search_only = Image.open(src_victory_points_search_only).convert('RGB')

            diff = ImageChops.difference(img_victory_points_search_only, img_victory_points)
            self.assertIsNotNone(diff.getbbox())

        # Satisfied, the user closes the app.
