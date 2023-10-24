from rest_framework.routers import DefaultRouter
from api import viewsets

router = DefaultRouter()
router.register('rooms', viewsets.RoomViewSets, basename='rooms')
router.register('guests', viewsets.GuestViewSets, basename='guests')
router.register('bookings', viewsets.BookingViewSets, basename='bookings')
router.register('bookings-users', viewsets.BookingUserViewSets, basename='bookings-users')
urlpatterns = router.urls