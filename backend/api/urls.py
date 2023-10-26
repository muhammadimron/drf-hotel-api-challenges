from rest_framework.routers import SimpleRouter
from api import viewsets

router = SimpleRouter()
router.register(r'rooms', viewsets.RoomViewSets, basename="rooms")
router.register(r'guests', viewsets.GuestViewSets, basename="guests")
router.register(r'bookings', viewsets.BookingViewSets, basename="bookings")
router.register(r'bookings-users', viewsets.BookingUserViewSets, basename="bookings-users")
urlpatterns = router.urls