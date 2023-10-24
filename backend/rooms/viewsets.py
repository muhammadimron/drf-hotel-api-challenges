from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .models import Room
from .serializers import RoomSeliazer

class RoomViewSets(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSeliazer
    lookup_field = 'pk'

    def perform_create(self, serializer):
        floor = serializer.validated_data.get('floor')
        number = serializer.validated_data.get('number')
        if floor:
            duplicate = Room.objects.filter(floor=floor, number=number).first()
            if duplicate:
                raise ValidationError(f"Room number {floor} in floor {number} has existed")
        serializer.save()

room_viewsets = RoomViewSets.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy'
})