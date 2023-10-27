from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class TestRoomViewSets(APITestCase):
    def setUp(self):
        self.url = "/rooms/"
        self.author = User.objects.create_superuser(username="admin", password="123")

    def login(self):
        self.client.force_login(user=self.author)

    def auth_assert(self, response):
        message = str(response.data["detail"])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(message, 'Authentication credentials were not provided.')

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

    def test_post_room_viewsets_without_authorization(self):
        response = self.post_data(floor=1, number=1)
        self.auth_assert(response=response)

    def test_post_room_viewsets_with_authorization(self):
        self.login()
        response = self.post_data(floor=1, number=1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_room_viewsets_without_authorization(self):
        self.input_data()
        response = self.get_data()
        self.auth_assert(response=response)
        
    def test_get_room_viewsets_with_authorization(self):
        self.login()
        self.input_data()
        response = self.get_data()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_room_viewsets_without_authorization(self):
        self.input_data()
        response = self.get_data_detail(id=3)
        self.auth_assert(response=response)

    def test_get_detail_room_viewsets_with_authorization(self):
        self.login()
        self.input_data()
        response = self.get_data_detail(id=3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_room_viewsets_without_authorization(self):
        self.input_data()
        response = self.put_data(id=3, floor=1, number=6)
        self.auth_assert(response=response)

    def test_put_room_viewsets_with_authorization(self):
        self.login()
        self.input_data()
        response = self.put_data(id=3, floor=1, number=6)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_del_room_viewsets_without_authorization(self):
        self.input_data()
        response = self.del_data(id=3)
        self.auth_assert(response=response)

    def test_del_room_viewsets_with_authorization(self):
        self.login()
        self.input_data()
        response = self.del_data(id=3)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)