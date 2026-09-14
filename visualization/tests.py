from django.test import TestCase


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_renders_form(self):
        response = self.client.get("/")
        self.assertContains(response, '<form method="POST">')
        self.assertContains(response, '<input id="search"')