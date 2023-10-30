from django.db import models
from .guests_model import Guest

class NewsletterSubscription(models.Model):
    guest_id = models.OneToOneField(Guest, on_delete=models.CASCADE)