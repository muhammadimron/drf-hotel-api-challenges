from rest_framework import authentication, permissions, viewsets

from api.authentication import BearerAuthentication
from api.models import Guest
from api.serializers import GuestSerializer

class GuestViewSets(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, BearerAuthentication]
    permission_classes = [permissions.IsAuthenticated]

