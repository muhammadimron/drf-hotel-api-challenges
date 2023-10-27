from rest_framework import viewsets, status
from rest_framework import authentication, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.authentication import BearerAuthentication
from api.models import Room
from api.serializers import RoomSeliazer

class RoomViewSets(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSeliazer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, BearerAuthentication]
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

    @action(methods=["GET"], detail=False)
    def add(self, request, *args, **kwargs):
        Room.objects.all().delete()
        for i in range(1, 6):
            for j in range(1, 6):
                serializer = RoomSeliazer(data={
                    "floor": i,
                    "number": j
                })
                serializer.is_valid()
                serializer.save()
        return Response({
            "success": "please hit http://127.0.0.1:8000/rooms/ to see the result.",
        }, status=status.HTTP_200_OK)

room_viewsets = RoomViewSets.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy'
})