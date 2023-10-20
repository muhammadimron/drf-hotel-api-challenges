from rest_framework import serializers
from .models import Room

class RoomSeliazer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = [
            'id',
            'number',
            'floor'
        ]

class RoomDetailSerializer(serializers.Serializer):
    number = serializers.IntegerField(read_only=True)
    floor = serializers.IntegerField(read_only=True)