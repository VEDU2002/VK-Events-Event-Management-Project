from django.contrib import admin
from eventapp.models import Event,Booking,SubCard
# Register your models here.
admin.site.register(Event)
admin.site.register(Booking)
admin.site.register(SubCard)