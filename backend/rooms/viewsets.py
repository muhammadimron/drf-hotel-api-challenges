from rest_framework import viewsets

from .models import Room
from .serializers import RoomSeliazer

class RoomViewSets(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSeliazer
    lookup_field = 'pk'

room_viewsets = RoomViewSets.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy'
})