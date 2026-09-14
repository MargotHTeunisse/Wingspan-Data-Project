from django.test import TestCase


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_renders_form(self):
        response = self.client.get("/")
        self.assertContains(response, '<form method="POST">')
        self.assertContains(response, '<input id="search"')

    def test_can_save_a_post_request(self):
        response = self.client.post("/", data={"scientific_name": "Limosa limosa"})
        self.assertContains(response, "Limosa limosa")
        self.assertTemplateUsed(response, "home.html")