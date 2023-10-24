from django.core.exceptions import ValidationError
from rest_framework import serializers
from api.models import Room
from api.validators import floor_max_length, number_max_length

class RoomSeliazer(serializers.ModelSerializer):
    floor = serializers.IntegerField(validators=[floor_max_length])
    number = serializers.IntegerField(validators=[number_max_length])
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