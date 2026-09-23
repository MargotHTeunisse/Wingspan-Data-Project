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

class DistributionAPITest(TestCase):
    def test_can_request_victory_points_distribution(self):
        response = self.client.get('/api/distribution?property=victory_points',
                                   content_type='application/json').json()

        self.assertIn('distribution', response)

    def test_can_request_wingspan_distribution(self):
        response = self.client.get('/api/distribution?property=wingspan',
                                   content_type='application/json').json()

        self.assertIn('distribution', response)

    def test_can_request_nest_capacity_distribution(self):
        response = self.client.get('/api/distribution?property=nest_capacity',
                                   content_type='application/json').json()

        self.assertIn('distribution', response)

    def test_can_retrieve_victory_points_data(self):
        # Test data
        for (scientific_name, vp) in (
                zip(['Limosa limosa', 'Falco peregrinus', 'Falco subbuteo'],
                                 [6, 5, 4])):
            bird = Bird()
            bird.scientific_name = scientific_name
            bird.victory_points = vp
            bird.save()

        response = self.client.get('/api/distribution?property=victory_points',
                                   content_type='application/json').json()

        self.assertEqual(response['distribution']['values'], [4, 5, 6])
        self.assertEqual(response['distribution']['counts'], [1, 1, 1])

    def test_can_retrieve_nest_capacity_data(self):
        # Test data
        for (scientific_name, nc) in (
                zip(['Limosa limosa', 'Falco peregrinus', 'Falco subbuteo'],
                                 [2, 2, 2])):
            bird = Bird()
            bird.scientific_name = scientific_name
            bird.nest_capacity = nc
            bird.save()

        response = self.client.get('/api/distribution?property=nest_capacity',
                                   content_type='application/json').json()

        self.assertEqual(response['distribution']['values'], [2])
        self.assertEqual(response['distribution']['counts'], [3])

    def test_can_retrieve_wingspan_data(self):
        # Test data
        for (scientific_name, ws) in (
                zip(['Limosa limosa', 'Falco peregrinus', 'Falco subbuteo'],
                                 [76, 104, 75])):
            bird = Bird()
            bird.scientific_name = scientific_name
            bird.wingspan = ws
            bird.save()

        response = self.client.get('/api/distribution?property=wingspan',
                                   content_type='application/json').json()

        self.assertEqual(response['distribution']['values'], [75, 76, 104])
        self.assertEqual(response['distribution']['counts'], [1, 1, 1])

def test_forbidden_property_request_raises_bad_request_error(self):
    invalid_response = self.client.get('/api/distribution?property=forbidden')

    self.assertEqual(invalid_response.status_code, 400)

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
