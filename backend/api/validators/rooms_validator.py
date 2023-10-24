from rest_framework import serializers

def floor_max_length(value):
    if value > 20:
        raise serializers.ValidationError(f"Floor must not exceed 20. Your input is {value}")
    return value

def number_max_length(value):
    if value > 50:
        raise serializers.ValidationError(f"Room number must not exceed 50. Your input is {value}")
    return value