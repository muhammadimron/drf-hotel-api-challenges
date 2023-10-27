from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework.test import APITestCase
from api.models import Room, Guest

class TestBookingsModels(APITestCase):
    def setUp(self):
        self.url = "/bookings/"
        self.bookings_users_url = "/bookings-users/"
        self.rooms_url = "/rooms/"
        self.guests_url = "/guests/"
        self.author = User.objects.create_superuser(username="admin", password="123")
        self.login()
        self.generate_rooms_and_guests()

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

    def get_data(self):
        return self.client.get(self.url)

    def get_detail_data(self, id):
        return self.client.get(self.url + f"{id}/")
    
    def put_data(self, id, room_id, guest_id):
        return self.client.put(self.url + f"{id}/", {
            "room_id": room_id,
            "guest_id": guest_id
        })

    def del_data(self, id, soft=False):
        return self.client.delete(self.url + f"{id}/") if not soft else self.client.delete(self.url +f"{id}/?soft=true")

    def input_data(self):
        for i in range(1, 6):
            room = Room.objects.get(id=i)
            guest = Guest.objects.get(id=i)
            self.post_data(room_id=room.id, guest_id=guest.id)
    
    def test_post_bookings_models(self):
        room = Room.objects.get(id=1)
        guest = Guest.objects.get(id=1)
        response = self.post_data(room_id=room.id, guest_id=guest.id)
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["room_id"], 1)
        self.assertEqual(data["room"], {
            "number": 1,
            "floor": 1
        })
        self.assertEqual(data["guest_id"], 1)
        self.assertEqual(data["guest"], {
            "name": "People 1"
        })
        self.assertFalse(data["is_deleted"])
        self.assertIsNone(data["deleted_at"])

    def test_get_bookings_models(self):
        self.input_data()
        response = self.get_data()
        data = response.json()
        self.assertEqual(len(data), 5)
        for i in range(1, 6):
            self.assertEqual(data[i-1]["id"], i)
            self.assertEqual(data[i-1]["room_id"], i)
            self.assertEqual(data[i-1]["room"], {
                "number": i,
                "floor": i
            })
            self.assertEqual(data[i-1]["guest_id"], i)
            self.assertEqual(data[i-1]["guest"], {
                "name": f"People {i}"
            })
            self.assertFalse(data[i-1]["is_deleted"])
            self.assertIsNone(data[i-1]["deleted_at"])

    def test_get_detail_bookings_models(self):
        self.input_data()
        response = self.get_detail_data(id=3)
        data = response.json()
        self.assertEqual(data["id"], 3)
        self.assertEqual(data["room_id"], 3)
        self.assertEqual(data["room"], {
            "number": 3,
            "floor": 3
        })
        self.assertEqual(data["guest_id"], 3)
        self.assertEqual(data["guest"], {
            "name": "People 3"
        })
        self.assertFalse(data["is_deleted"])
        self.assertIsNone(data["deleted_at"])

    def test_put_bookings_models(self):
        self.input_data()
        response = self.put_data(id=3, room_id=7, guest_id=9)
        data = response.json()
        self.assertEqual(data["id"], 3)
        self.assertEqual(data["room_id"], 7)
        self.assertEqual(data["room"], {
            "number": 7,
            "floor": 7
        })
        self.assertEqual(data["guest_id"], 9)
        self.assertEqual(data["guest"], {
            "name": "People 9"
        })
        self.assertFalse(data["is_deleted"])
        self.assertIsNone(data["deleted_at"])

    def test_del_bookings_models(self):
        self.input_data()
        self.del_data(id=3)
        data = [item for item in self.get_data().json() if item["id"] == 3]
        self.assertEqual(data, [])

    def test_soft_del_bookings_models(self):
        self.input_data()
        self.del_data(id=3, soft=True)
        data = [item for item in self.get_data().json() if item["id"] == 3]
        self.assertEqual(data[0]["id"], 3)
        self.assertEqual(data[0]["room_id"], 3)
        self.assertEqual(data[0]["room"], {
            "number": 3,
            "floor": 3
        })
        self.assertEqual(data[0]["guest_id"], 3)
        self.assertEqual(data[0]["guest"], {
            "name": "People 3"
        })
        self.assertTrue(data[0]["is_deleted"])