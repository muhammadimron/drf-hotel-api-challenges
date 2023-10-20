from rest_framework.routers import DefaultRouter
from guests.viewsets import GuestViewSets
from rooms.viewsets import RoomViewSets
from booking_details.viewsets import BookingViewSets, BookingUserViewSets

router = DefaultRouter()
router.register('rooms', RoomViewSets, basename='rooms')
router.register('guests', GuestViewSets, basename='guests')
router.register('bookings', BookingViewSets, basename='bookings')
router.register('bookings-users', BookingUserViewSets, basename='bookings-users')
urlpatterns = router.urls