from rest_framework import serializers
from .models import Guest
from .validators import unique_name_validator

class GuestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[unique_name_validator])
    class Meta:
        model = Guest
        fields = [
            'id',
            'name'
        ]

class GuestDetailSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)