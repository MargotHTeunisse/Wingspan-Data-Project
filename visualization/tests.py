from django.test import TestCase

from visualization.models import Bird


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")

        self.assertTemplateUsed(response, "home.html")

    def test_renders_form(self):
        response = self.client.get("/")

        self.assertContains(response, '<form method="POST">')
        self.assertContains(response, '<input id="search"')

    def test_can_retrieve_bird_by_full_name(self):
        black_tailed_godwit = Bird()
        black_tailed_godwit.scientific_name = "Limosa limosa"
        black_tailed_godwit.save()

        response = self.client.post("/",
                                    data={"scientific_name": black_tailed_godwit.scientific_name})

        self.assertContains(response, black_tailed_godwit.scientific_name)
        self.assertTemplateUsed(response, "home.html")

    def test_can_retrieve_bird_by_partial_name(self):
        black_tailed_godwit = Bird()
        black_tailed_godwit.scientific_name = "Limosa limosa"
        black_tailed_godwit.save()

        response = self.client.post("/",
                                    data={"scientific_name": "Limosa"})

        self.assertContains(response, "Limosa limosa")
        self.assertTemplateUsed(response, "home.html")


    def test_can_retrieve_different_bird_by_full_name(self):
        peregrine_falcon = Bird()
        peregrine_falcon.scientific_name = "Falco peregrinus"
        peregrine_falcon.save()

        response = self.client.post("/",
                                    data={"scientific_name": peregrine_falcon.scientific_name})

        self.assertContains(response, "Falco peregrinus")
        self.assertTemplateUsed(response, "home.html")

class BirdModelTest(TestCase):
    def test_saving_and_retrieving_birds(self):
        black_tailed_godwit = Bird()
        black_tailed_godwit.scientific_name = "Limosa limosa"
        black_tailed_godwit.save()

        peregrine_falcon = Bird()
        peregrine_falcon.scientific_name = "Falco peregrinus"
        peregrine_falcon.save()

        saved_birds = Bird.objects.all()
        self.assertEqual(saved_birds.count(), 2)

        first_bird = saved_birds[0]
        second_bird = saved_birds[1]
        self.assertEqual(first_bird.scientific_name, "Limosa limosa")
        self.assertEqual(second_bird.scientific_name, "Falco peregrinus")