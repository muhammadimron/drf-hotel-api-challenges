from django.contrib.auth.models import User
from rest_framework.test import APITestCase

class TestGuestModels(APITestCase):
    def setUp(self):
        self.url = "/guests/"
        self.author = User.objects.create_superuser(username="admin", password="123")
        self.login()

    def login(self):
        self.client.force_login(user=self.author)

    def post_data(self, name=""):
        return self.client.post(self.url, {
            "name": name
        })

    def get_data(self):
        return self.client.get(self.url)
    
    def get_detail_data(self, id=1):
        return self.client.get(self.url + f"{id}/")

    def put_data(self, id=1, name=""):
        return self.client.put(self.url + f"{id}/", {
            "name": name
        })
    
    def del_data(self, id=1):
        return self.client.delete(self.url + f"{id}/")

    def input_data(self):
        for i in range(1, 6):
            self.post_data(name=f"People {i}")

    def test_post_guest_models(self):
        response = self.post_data(name="Muhammad Imron")
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "Muhammad Imron")

    def test_get_guest_models(self):
        self.input_data()
        response = self.get_data()
        data = response.json()
        for i in range(1, 6):
            self.assertEqual(data[i-1]["id"], i)
            self.assertEqual(data[i-1]["name"], f"People {i}")

    def test_get_detail_guest_models(self):
        self.input_data()
        response = self.get_detail_data(id=2)
        data = response.json()
        self.assertEqual(data["id"], 2)
        self.assertEqual(data["name"], "People 2")

    def test_put_guest_models(self):
        self.input_data()
        response = self.put_data(id=3, name="Ahmad Jamaludin")
        data = response.json()
        self.assertEqual(data["id"], 3)
        self.assertEqual(data["name"], "Ahmad Jamaludin")

    def test_del_guest_models(self):
        self.input_data()
        self.del_data(id=3)
        data = [item for item in self.get_data().json() if item["id"] == 3]
        self.assertEqual(data, [])