from django.contrib import admin

from api.models import Booking, Guest, Room, NewsletterSubscription

# Register your models here.
admin.site.register(Booking)
admin.site.register(Guest)
admin.site.register(Room)
admin.site.register(NewsletterSubscription)