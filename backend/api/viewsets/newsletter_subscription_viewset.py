from rest_framework import authentication, permissions, viewsets
from rest_framework.response import Response

from api.authentication import BearerAuthentication
from api.models import Guest, NewsletterSubscription
from api.serializers import NewsletterSubscriptionSerializer

class NewsletterSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, BearerAuthentication]
    permission_classes = [permissions.IsAuthenticated]
