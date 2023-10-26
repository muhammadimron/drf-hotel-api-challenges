from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class TestRoomValidators(APITestCase):
    def setUp(self):
        self.url = "/api/rooms/"
        self.author = User.objects.create_superuser(username="admin", password="123")

    def login(self):
        self.client.force_login(user=self.author)

    def post_data(self, floor=0, number=0):
        return self.client.post(self.url, {
            "floor": floor,
            "number": number
        })

    def put_data(self, id=1, floor=0, number=0):
        return self.client.put(self.url + f"{id}/", {
            "floor": floor,
            "number": number
        })
    
    def input_data(self):
        for i in range(1, 6):
            self.post_data(floor=1, number=i)

    def test_post_validators(self):
        self.login()
        self.input_data()
        
        res_existed_floor_number = self.post_data(floor=1, number=1)
        self.assertEqual(res_existed_floor_number.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_existed_floor_number.json()[0], "Room number 1 in floor 1 has existed")
        
        res_max_floor = self.post_data(floor=21, number=1)
        self.assertEqual(res_max_floor.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_max_floor.json()["floor"][0], "Floor must not exceed 20. Your input is 21")
        
        res_max_number = self.post_data(floor=1, number=51)
        self.assertEqual(res_max_number.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_max_number.json()["number"][0], "Room number must not exceed 50. Your input is 51")

    def test_put_validator(self):
        self.login()
        self.input_data()

        res_existed_floor_number = self.put_data(id=2, floor=1, number=1)
        self.assertEqual(res_existed_floor_number.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_existed_floor_number.json()[0], "Room number 1 in floor 1 has existed")
        
        res_max_floor = self.put_data(id=2, floor=21, number=1)
        self.assertEqual(res_max_floor.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_max_floor.json()["floor"][0], "Floor must not exceed 20. Your input is 21")
        
        res_max_number = self.put_data(id=2, floor=1, number=51)
        self.assertEqual(res_max_number.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_max_number.json()["number"][0], "Room number must not exceed 50. Your input is 51")