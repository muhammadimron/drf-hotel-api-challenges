from rest_framework.routers import SimpleRouter
from api import viewsets

router = SimpleRouter()
router.register(r'rooms', viewsets.RoomViewSets, basename="rooms")
router.register(r'guests', viewsets.GuestViewSets, basename="guests")
router.register(r'bookings', viewsets.BookingViewSets, basename="bookings")
router.register(r'bookings-users', viewsets.BookingUserViewSets, basename="bookings-users")
router.register(r'subcriber', viewsets.NewsletterSubscriptionViewSet, basename="subcriber")
router.register(r'changed-log', viewsets.ChangedLogViewSet, basename="changed-log")
router.register(r'export-excel-bookings-v2', viewsets.BookingExportXLSXViewSets, basename="export-excel-bookings-v2")
urlpatterns = router.urls