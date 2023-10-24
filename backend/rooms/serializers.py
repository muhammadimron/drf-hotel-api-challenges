from django.core.exceptions import ValidationError
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

    def clean(self):
        floor = self.validated_data.get('floor')
        number = self.validated_data.get('number')
        if floor:
            duplicate = Room.objects.filter(floor=floor, number=number).first()
            if duplicate:
                raise ValidationError(f"Room number {floor} in floor {number} has existed")

class RoomDetailSerializer(serializers.Serializer):
    number = serializers.IntegerField(read_only=True)
    floor = serializers.IntegerField(read_only=True)