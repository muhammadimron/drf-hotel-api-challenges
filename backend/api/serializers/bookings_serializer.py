from rest_framework import serializers

from .guests_serializer import GuestDetailSerializer
from .rooms_serializer import RoomDetailSerializer

from api.models import Booking

class BookingSerializer(serializers.ModelSerializer):
    room = RoomDetailSerializer(source='room_id', read_only=True)
    guest = GuestDetailSerializer(source='guest_id', read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'start_date',
            'end_date',
            'room_id',
            'room',
            'guest_id',
            'guest',
            'is_deleted',
            'deleted_at'
        ]