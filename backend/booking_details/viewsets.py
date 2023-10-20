from rest_framework import viewsets

from .models import Booking
from .serializers import BookingSerializer

class BookingViewSets(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        hard = self.request.query_params.get('hard')
        instance.delete(hard)

class BookingUserViewSets(viewsets.ReadOnlyModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Booking.objects.filter(is_deleted=False)