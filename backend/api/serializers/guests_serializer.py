from rest_framework import serializers
from api.models import Guest
from api.validators import unique_name_validator

class GuestSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[unique_name_validator])
    class Meta:
        model = Guest
        fields = [
            'id',
            'name',
            'email'
        ]

class GuestDetailSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)