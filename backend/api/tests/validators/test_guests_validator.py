from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class TestGuestValidators(APITestCase):
    def setUp(self):
        self.url = "/guests/"
        self.author = User.objects.create_superuser(username="admin", password="123")
        self.login()
        self.input_data()

    def login(self):
        self.client.force_login(user=self.author)

    def post_data(self, name=""):
        return self.client.post(self.url, {
            "name": name
        })

    def put_data(self, id=1, name=""):
        return self.client.put(self.url + f"{id}/", {
            "name": name
        })

    def input_data(self):
        for i in range(1, 6):
            self.post_data(name=f"People {i}")

    def test_post_validator(self):
        response = self.post_data(name="People 1")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["name"][0], "This field must be unique.")

    def test_put_validator(self):
        response = self.put_data(id=1, name="People 4")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["name"][0], "This field must be unique.")
