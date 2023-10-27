from rest_framework import authentication, permissions, viewsets
from rest_framework.exceptions import ValidationError

from api.authentication import BearerAuthentication
from api.models import Booking
from api.serializers import BookingSerializer

class BookingViewSets(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, BearerAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def shared_logic(self, validated_data=None, method=None):
        room_id = validated_data.get('room_id')
        guest_id = validated_data.get('guest_id')
        if room_id:
            duplicate_room_id = Booking.objects.filter(room_id=room_id)
            if duplicate_room_id:
                raise ValidationError("You cannot bookings the ordered room")
        if guest_id:
            duplicate_guest_id = Booking.objects.filter(guest_id=guest_id)
            if duplicate_guest_id:
                raise ValidationError("You cannot ordered more than one room")
        return validated_data

    def perform_create(self, serializer):
        validated_data = self.shared_logic(validated_data=serializer.validated_data)
        serializer.save(**validated_data)
    
    def perform_update(self, serializer):
        validated_data = self.shared_logic(validated_data=serializer.validated_data, method='PUT')
        serializer.save(**validated_data)

    def perform_destroy(self, instance):
        soft = self.request.query_params.get('soft')
        instance.delete(soft)

class BookingUserViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, BearerAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(is_deleted=False)