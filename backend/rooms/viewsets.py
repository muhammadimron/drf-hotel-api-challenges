from rest_framework import viewsets
from rest_framework import authentication, permissions
from rest_framework.exceptions import ValidationError

from backend.authentication import TokenAuthentication
from .models import Room
from .serializers import RoomSeliazer

class RoomViewSets(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSeliazer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def shared_logic(self, validated_data=None):
        floor = validated_data.get('floor')
        number = validated_data.get('number')
        if floor:
            duplicate = Room.objects.filter(floor=floor, number=number).first()
            if duplicate:
                raise ValidationError(f"Room number {floor} in floor {number} has existed")
        return validated_data

    def perform_create(self, serializer):
        validated_data = self.shared_logic(validated_data=serializer.validated_data)
        serializer.save(**validated_data)

    def perform_update(self, serializer):
        validated_data = self.shared_logic(validated_data=serializer.validated_data)
        serializer.save(**validated_data)

room_viewsets = RoomViewSets.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy'
})