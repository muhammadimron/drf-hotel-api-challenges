from rest_framework import authentication, permissions, viewsets

from backend.authentication import TokenAuthentication
from .models import Guest
from .serializers import GuestSerializer

class GuestViewSets(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

