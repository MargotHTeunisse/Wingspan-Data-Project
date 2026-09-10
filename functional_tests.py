from selenium import webdriver
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
        self.fail("Finish the test!")

        ##Now they want to check that the black-tailed godwit is represented accurately.
        ##They check that the bird:
        ##- lives in wetlands
        ##- nests on the ground
        ##- eats bugs and grains
        ##- has a wingspan of 76 cm

        ##They notice that it has a nest capacity of 2.
        ##That number doesn't tell them much; they need to see how this compares to other birds.
        ##They plot the nest capacities, and find that 2 is the median nest capacity.

        ##While they make this plot, they still want to keep the black-tailed godwit in view.

        ##They notice that the bird is worth 6 victory points. They wonder what that value is based on.
        ##The black-tailed godwit has 3 food tokens.
        ##Perhaps birds are worth more points the more food they require?
        ##They make a bar chart to check this.

        ##Satisfied, they close the application.





