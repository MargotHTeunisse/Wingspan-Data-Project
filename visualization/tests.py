from django.test import TestCase
from parameterized import parameterized

from visualization.models import Bird


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")

        self.assertTemplateUsed(response, "home.html")

    def test_renders_form(self):
        response = self.client.get("/")

        self.assertContains(response, '<form method="GET">')
        self.assertContains(response, '<input id="search"')

    def test_home_template_is_used(self):
        response = self.client.get("/", data={"scientific_name": "Limosa limosa"})

        self.assertTemplateUsed(response, "home.html")

    @parameterized.expand(
                             [
                                 ["Limosa limosa", "Limosa limosa"],
                                 ["Limosa limosa", "Limosa"],
                                 ["Falco peregrinus", "Falco peregrinus"],
                                 ["Falco peregrinus", "Falco"],
                                 ["Falco peregrinus", "fALcO"]
                             ])
    def test_can_retrieve_bird(self, scientific_name:str, query:str):
        bird = Bird()
        bird.scientific_name = scientific_name
        bird.save()

        response = self.client.get("/",
                                    data={"scientific_name": query})

        self.assertTrue(bird in response.context['search_results'])

class BirdModelTest(TestCase):
    def test_can_save_multiple_birds(self):
        black_tailed_godwit = Bird()
        black_tailed_godwit.scientific_name = "Limosa limosa"
        black_tailed_godwit.save()

        peregrine_falcon = Bird()
        peregrine_falcon.scientific_name = "Falco peregrinus"
        peregrine_falcon.save()

        saved_birds = Bird.objects.all()
        self.assertEqual(saved_birds.count(), 2)

    @parameterized.expand([
                    ["Limosa limosa"],
                    ["Falco peregrinus"]
                ])
    def test_saving_and_retrieving_single_bird(self, scientific_name:str):
        bird = Bird()
        bird.scientific_name = scientific_name
        bird.save()

        saved_birds = Bird.objects.all()

        self.assertEqual(saved_birds[0].scientific_name, scientific_name)
