from django.db import models

# Create your models here.
class Event(models.Model):
    img=models.ImageField(upload_to="pic")
    name=models.CharField(max_length=50)
    desc=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class Booking(models.Model):
    cus_name = models.CharField(max_length=55)
    cus_phone = models.CharField(max_length=15, verbose_name="Customer Phone")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # only this one
    booking_date = models.DateField()
    booked_on = models.DateField(auto_now=True)


class SubCard(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='subcards')
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='subcard_images/', blank=True, null=True) 

    def __str__(self):
        return self.title
    