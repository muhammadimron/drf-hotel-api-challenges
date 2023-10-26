from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class TestGuestViewSets(APITestCase):
    def setUp(self):
        self.url = "/api/guests/"
        self.author = User.objects.create_superuser(username="admin", password="123")

    def login(self):
        self.client.force_login(user=self.author)

    def auth_assert(self, response):
        message = str(response.data["detail"])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(message, 'Authentication credentials were not provided.')

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

    def del_data(self, id=0):
        return self.client.delete(self.url + f"{id}/")

    def input_data(self):
        for i in range(1, 6):
            self.post_data(name=f"People {i}")

    def test_post_guests_viewset_without_authorization(self):
        response = self.post_data(name="People 1")
        self.auth_assert(response=response)

    def test_post_guests_viewset_with_authorization(self):
        self.login()
        response = self.post_data(name="People 1")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_guests_viewset_without_authorization(self):
        self.input_data()
        response = self.get_data()
        self.auth_assert(response=response)
    
    def test_get_guest_viewset_with_authorization(self):
        self.login()
        self.input_data()
        response = self.get_data()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_guest_viewset_without_authorization(self):
        self.input_data()
        response = self.get_detail_data(id=3)
        self.auth_assert(response=response)

    def test_get_detail_guest_viewset_with_authorization(self):
        self.login()
        self.input_data()
        response = self.get_detail_data(id=3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_guest_viewset_without_authorization(self):
        self.input_data()
        response = self.put_data(id=3, name="Muhammad Imron")
        self.auth_assert(response=response)

    def test_put_guest_viewset_with_authorization(self):
        self.login()
        self.input_data()
        response = self.put_data(id=3, name="Muhammad Imron")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_del_guest_viewset_without_authorization(self):
        self.input_data()
        response = self.del_data(id=3)
        self.auth_assert(response=response)

    def test_del_guest_viewset_with_authorization(self):
        self.login()
        self.input_data()
        response = self.del_data(id=3)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)