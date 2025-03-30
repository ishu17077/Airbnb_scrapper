from django.db import models

# Create your models here.
class AirbnbListing(models.Model):
   title = models.TextField()
   fullUrl = models.URLField()
   images = models.JSONField()
   avgRating = models.TextField()
   pricePerNight = models.TextField()
   totalPrice = models.TextField()




