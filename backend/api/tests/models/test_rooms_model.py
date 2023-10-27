from django.contrib.auth.models import User
from rest_framework.test import APITestCase

class TestRoomModels(APITestCase):
    def setUp(self):
        self.url = "/rooms/"
        self.author = User.objects.create_superuser(username="admin", password="123")
        self.login()

    def login(self):
        self.client.force_login(user=self.author)

    def post_data(self, floor=0, number=0):
        return self.client.post(self.url, {
            "floor": floor,
            "number": number
        })

    def get_data(self):
        return self.client.get(self.url)

    def get_data_detail(self, id=1):
        return self.client.get(self.url + f"{id}/", )

    def put_data(self, id=1, floor=0, number=0):
        return self.client.put(self.url + f"{id}/", {
            "floor": floor,
            "number": number
        })

    def del_data(self, id=0):
        return self.client.delete(self.url + f"{id}/")
    
    def input_data(self):
        for i in range(1, 6):
            self.post_data(floor=1, number=i)
            
    def test_post_room_models(self):
        response = self.post_data(floor=1, number=1)
        self.assertEqual(response.json()["id"], 1)
        self.assertEqual(response.json()["number"], 1)
        self.assertEqual(response.json()["floor"], 1)
        
    def test_get_room_models(self):
        self.input_data()
        response = self.get_data()
        data = response.json()
        for i in range(1, 6):
            self.assertEqual(data[i-1]["id"], i)
            self.assertEqual(data[i-1]["number"], i)
            self.assertEqual(data[i-1]["floor"], 1)

    def test_get_detail_room_models(self):
        self.login()
        self.input_data()
        response = self.get_data_detail(id=3)
        data = response.json()
        self.assertEqual(data["id"], 3)
        self.assertEqual(data["number"], 3)
        self.assertEqual(data["floor"], 1)

    def test_put_room_models(self):
        self.login()
        self.input_data()
        response = self.put_data(id=3, floor=1, number=6)
        data = response.json()
        self.assertEqual(data["id"], 3)
        self.assertEqual(data["number"], 6)
        self.assertEqual(data["floor"], 1)

    def test_del_room_models(self):
        self.login()
        self.input_data()
        self.del_data(id=3)
        data = [item for item in self.get_data().json() if item["id"] == 3]
        self.assertEqual(data, [])