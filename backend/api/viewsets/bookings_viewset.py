from django.utils.timezone import now

from rest_framework import authentication, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.authentication import BearerAuthentication
from api.models import Booking, Guest, Room
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

    @action(methods=["GET"], detail=False)
    def add(self, request, *args, **kwargs):
        Booking.objects.all().delete()
        for i in range(1, 6):
            room = Room.objects.filter(floor=1, number=i).first()
            guest = Guest.objects.filter(name=f"People number {i}").first()
            serializer = BookingSerializer(data={
                ""
                "room_id": room.id,
                "guest_id": guest.id
            })
            serializer.is_valid()
            serializer.save()
        return Response({
            "success": "please hit http://127.0.0.1:8000/bookings/ to see the result."
        }, status=status.HTTP_200_OK)

class BookingUserViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, BearerAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(is_deleted=False)