from django.db import models
from django_softdelete.models import SoftDeleteModel
from django.utils import timezone

from .guests_model import Guest
from .rooms_model import Room

# Create your models here.
class Booking(SoftDeleteModel):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    room_id = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    guest_id = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True)
