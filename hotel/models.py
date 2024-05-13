from django.db import models

# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.TextField()
    stars =models.IntegerField(blank=False, null=False)
    address = models.TextField()
    country = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    state = models.CharField(max_length=100, blank=False, null=False)
    
    def __str__(self):
        return self.name
    