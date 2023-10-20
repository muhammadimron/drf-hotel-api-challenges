from rest_framework import viewsets

from .models import Guest
from .serializers import GuestSerializer

class GuestViewSets(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    lookup_field = 'pk'

