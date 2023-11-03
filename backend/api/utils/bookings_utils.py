from api.models import Booking, Guest, Room

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