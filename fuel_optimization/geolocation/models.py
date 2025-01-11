from django.db import models

# Create your models here.
class FuelStation(models.Model):
    truckstop_id = models.IntegerField()
    truckstop_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    retail_price = models.FloatField()

    def __str__(self):
        return f"{self.truckstop_name} - {self.city}, {self.state}"