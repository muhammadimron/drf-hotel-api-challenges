from django.db import models

# Create your models here.
class Guest(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name
        