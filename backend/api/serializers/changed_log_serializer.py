from rest_framework import serializers
from api.models import ChangedLog

class ChangedLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangedLog
        fields = "__all__"