from django.db import models
from django.utils import timezone

from guests.models import Guest
from rooms.models import Room

# Create your models here.
class Booking(models.Model):
    start_date = models.DateTimeField(default=timezone.now())
    end_date = models.DateTimeField(default=timezone.now())
    room_id = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    guest_id = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    def delete(self, hard=False):
        if hard:
            return super().delete()
        else:
            self.is_deleted = True
            self.deleted_at = timezone.now()
            return super().save()
