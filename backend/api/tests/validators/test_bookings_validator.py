from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Room, Guest

class TestBookingsValidator(APITestCase):
    def setUp(self):
        self.url = "/bookings/"
        self.rooms_url = "/rooms/"
        self.guests_url = "/guests/"
        self.author = User.objects.create_superuser(username="admin", password="123")
        self.login()
        self.generate_rooms_and_guests()
        self.input_data()

    def login(self):
        self.client.force_login(user=self.author)

    def generate_rooms_and_guests(self):
        for i in range(1, 11):
            self.client.post(self.rooms_url, {
                "floor": i,
                "number": i
            })
            self.client.post(self.guests_url, {
                "name": f"People {i}"
            })

    def post_data(self, room_id, guest_id):
        return self.client.post(self.url, {
            "start_date": now(),
            "end_date": now(),
            "room_id": room_id,
            "guest_id": guest_id
        })

    def put_data(self, id, room_id=None, guest_id=None):
        if room_id:
            return self.client.put(self.url + f"{id}/", {
                "room_id": room_id,
                "guest_id": guest_id
            })
        else:
            return self.client.put(self.url + f"{id}/", {
                "guest_id": guest_id
            })

    def input_data(self):
        self.generate_rooms_and_guests()
        for i in range(1, 6):
            room = Room.objects.get(id=i)
            guest = Guest.objects.get(id=i)
            self.post_data(room_id=room.id, guest_id=guest.id)

    def test_post_validators(self):
        response_same_rooms = self.post_data(room_id=1, guest_id=7)
        self.assertEqual(response_same_rooms.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_same_rooms.json()[0], "You cannot bookings the ordered room")
        response_same_guests = self.post_data(room_id=7, guest_id=1)
        self.assertEqual(response_same_rooms.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_same_guests.json()[0], "You cannot ordered more than one room")

    def test_put_validators(self):
        response_same_rooms = self.put_data(id=2, room_id=4, guest_id=2)
        self.assertEqual(response_same_rooms.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_same_rooms.json()[0], "You cannot bookings the ordered room")
        response_same_guest = self.put_data(id=2, guest_id=4)
        self.assertEqual(response_same_guest.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_same_guest.json()[0], "You cannot ordered more than one room")