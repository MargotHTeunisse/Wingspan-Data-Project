from django.test import TestCase
from django.http import HttpRequest
from visualization.views import home_page

class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertContains(response, "<title>Wingspan data visualization</title>")
        self.assertContains(response, "<html>")
        self.assertContains(response, "</html>")