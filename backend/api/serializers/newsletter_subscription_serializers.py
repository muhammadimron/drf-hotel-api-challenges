from rest_framework import serializers
from api.models import NewsletterSubscription
from .guests_serializer import GuestSerializer

class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    subscriber = GuestSerializer(source="guest_id", read_only=True)
    class Meta:
        model = NewsletterSubscription
        fields = [
            'id',
            'guest_id',
            'subscriber'
        ]
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if self.context['request'].method not in ['POST', 'PUT']:
            rep.pop('guest_id', None)
        return rep