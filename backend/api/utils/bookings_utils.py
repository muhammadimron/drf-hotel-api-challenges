from api.models import Booking, Guest, Room

import seaborn as sns
import matplotlib.pyplot as plt

from collections import Counter

def get_bookings_row():
    bookings = Booking.objects.all()
    rows = []
    for booking in bookings.values():
        if booking["is_deleted"]:
            continue
        guest = Guest.objects.filter(id=booking["guest_id_id"]).values().first()
        room = Room.objects.filter(id=booking["room_id_id"]).values().first()
        row = {}
        row["ID"] = booking["id"]
        row["GuestName"] = guest["name"]
        row["BookingRoom"] = f"Room in floor {room['floor']}, number {room['number']}"
        row["StartDate"] = booking["start_date"].strftime("%B %d, %Y")
        row["EndDate"] = booking["end_date"].strftime("%B %d, %Y")
        rows.append(row)
    return rows

def get_bookings_list():
    bookings = Booking.objects.all()
    rows = [["ID", "GuestName", "BookingRoom", "StartDate", "EndDate"]]
    for booking in bookings.values():
        if booking["is_deleted"]:
            continue
        guest = Guest.objects.filter(id=booking["guest_id_id"]).values().first()
        room = Room.objects.filter(id=booking["room_id_id"]).values().first()
        row = []
        row.append(booking["id"])
        row.append(guest["name"])
        row.append(f"Room in floor {room['floor']}, number {room['number']}")
        row.append(booking["start_date"].strftime("%B %d, %Y"))
        row.append(booking["end_date"].strftime("%B %d, %Y"))
        rows.append(row)
    return rows

def set_chart_bookings():
    floors = sorted([item["floor"] for item in Room.objects.all().values("floor").distinct()])
    bookings_room_in_each_floor = Counter(item["room_id__floor"] for item in Booking.objects.filter(is_deleted=False).values("room_id__floor"))
    _render_chart_bookings(floors, [bookings_room_in_each_floor[floor] for floor in floors])    

def _render_chart_bookings(categories, values):
    custom_palette = ["#1976d2", "#c2614e", "#d4cf3f", "#68eb4d", "#d64deb"]
    sns.set(style="whitegrid")
    plt.figure(figsize=(8,6))
    sns.barplot(x=categories, y=values, palette=custom_palette)

    plt.xlabel("Floor")
    plt.ylabel("Booking Rooms")
    plt.title("Booking Rooms in each Floor")

    plt.savefig("./api/static/chart.png", format="png")