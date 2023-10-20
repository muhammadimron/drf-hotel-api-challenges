from rest_framework import serializers
from .models import Guest

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = [
            'id',
            'name'
        ]

class GuestDetailSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)