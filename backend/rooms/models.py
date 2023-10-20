from django.db import models

# Create your models here.
class Room(models.Model):
    number = models.IntegerField()
    floor = models.IntegerField()

    def __str__(self):
        return f'Room number {self.number} in floor {self.floor}'