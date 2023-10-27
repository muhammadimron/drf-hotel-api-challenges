from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Room, Guest

class TestBookingsViewSets(APITestCase):
    def setUp(self):
        self.url = "/bookings/"
        self.bookings_user_url = "/bookings-users/"
        self.room_url = "/rooms/"
        self.guest_url = "/guests/"
        self.author = User.objects.create_superuser(username="admin", password="123")
        
    def generate_room_and_guest(self):
        for i in range(1, 11):
            self.client.post(self.room_url, {
                "floor": i,
                "number": i
            })
            
            self.client.post(self.guest_url, {
                "name": f"People {i}"
            })

    def login(self):
        self.client.force_login(user=self.author)


    def auth_assert(self, response):
        message = str(response.data["detail"])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(message, 'Authentication credentials were not provided.')

    def post_data(self, room_id, guest_id):
        return self.client.post(self.url, {
            "start_date": now(),
            "end_date": now(),
            "room_id": guest_id,
            "guest_id": room_id,

        })

    def get_data(self, url):
        return self.client.get(url)

    def get_detail_data(self, url, id=1):
        return self.client.get(url + f"{id}/")

    def put_data(self, room_id, guest_id, id=1):
        return self.client.put(self.url + f"{id}/", {
            "room_id": room_id,
            "guest_id": guest_id
        })

    def del_data(self, id=1, soft=False):
        return self.client.delete(self.url + f"{id}/") if not soft else self.client.delete(self.url + f"{id}/?soft=true")

    def input_data(self):
        # breakpoint()
        self.generate_room_and_guest()
        for i in range(1, 6):
            room = Room.objects.get(id=i)
            guest = Guest.objects.get(id=i)
            self.post_data(room_id=room.id, guest_id=guest.id)

    def test_post_bookings_viewset_without_authorization(self):
        response = self.post_data(room_id=1, guest_id=1)
        self.auth_assert(response=response)

    def test_post_bookings_viewset_with_authorization(self):
        self.login()
        self.generate_room_and_guest()
        room = Room.objects.get(id=1)
        guest = Guest.objects.get(id=1)
        response = self.post_data(room_id=room.id, guest_id=guest.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_bookings_viewset_without_authorization(self):
        response = self.get_data(url=self.url)
        self.auth_assert(response=response)

    def test_get_bookings_viewset_with_authorization(self):
        self.login()
        self.input_data()
        response = self.get_data(url=self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_bookings_without_authorization(self):
        response = self.get_detail_data(url=self.url, id=3)
        self.auth_assert(response=response)

    def test_get_detail_bookings_with_authorization(self):
        self.login()
        self.input_data()
        response = self.get_detail_data(self.url, id=3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_bookings_without_authorization(self):
        response = self.put_data(id=3, room_id=2, guest_id=2)
        self.auth_assert(response=response)

    def test_put_bookings_with_authorization(self):
        self.login()
        self.input_data()
        room = Room.objects.create(floor=15, number=15)
        guest = Guest.objects.create(name="Muhammad Imron")
        response = self.put_data(id=3, room_id=room.id, guest_id=guest.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_del_bookings_without_authorization(self):
        response = self.del_data(id=2)
        self.auth_assert(response=response)

    def test_del_bookings_with_authorization(self):
        self.login()
        self.input_data()
        response = self.del_data(id=3)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_bookings_user_without_authorization(self):
        response = self.get_data(url=self.bookings_user_url)
        self.auth_assert(response=response)

    def test_get_bookings_user_with_authorization(self):
        self.login()
        self.input_data()
        response = self.get_data(url=self.bookings_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_bookings_user_without_authorization(self):
        response = self.get_data(url=self.bookings_user_url)
        self.auth_assert(response=response)
    
    def test_get_detail_bookings_user_with_authorization(self):
        self.login()
        self.input_data()
        response = self.get_data(url=self.bookings_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_soft_delete_bookings_without_authorization(self):
        response = self.del_data(id=3, soft=True)
        self.auth_assert(response=response)

    def test_soft_delete_bookings_with_authorization(self):
        self.login()
        self.input_data()
        response = self.del_data(id=3, soft=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)