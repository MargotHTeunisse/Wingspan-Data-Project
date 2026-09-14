from django.test import TestCase


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_renders_form(self):
        response = self.client.get("/")
        self.assertContains(response, '<form method="POST">')
        self.assertContains(response, '<input id="search"')

    def test_can_retrieve_bird_by_full_name(self):
        response = self.client.post("/", data={"scientific_name": "Limosa limosa"})
        self.assertContains(response, "Limosa limosa")
        self.assertTemplateUsed(response, "home.html")

    def test_can_retrieve_bird_by_partial_name(self):
        response = self.client.post("/", data={"scientific_name": "Limosa"})
        self.assertContains(response, "Limosa limosa")
        self.assertTemplateUsed(response, "home.html")


    def test_can_retrieve_different_bird_by_full_name(self):
        response = self.client.post("/", data={"scientific_name": "Falco peregrinus"})
        self.assertContains(response, "Falco peregrinus")
        self.assertTemplateUsed(response, "home.html")