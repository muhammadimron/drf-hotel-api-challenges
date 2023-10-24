from rest_framework import viewsets
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError

from .models import Room
from .serializers import RoomSeliazer

class RoomViewSets(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSeliazer
    lookup_field = 'pk'

    def perform_create(self, serializer):
        try:
            serializer.clean()
            if serializer.is_valid():
                serializer.save()
        except ValidationError as e:
            raise DRFValidationError({'detail': e.messages[0]})

room_viewsets = RoomViewSets.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy'
})