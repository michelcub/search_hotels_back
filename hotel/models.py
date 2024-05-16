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
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    
    def __str__(self):
        return self.name


class Services(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    img = models.URLField(null=True, blank=True, default='https://th.bing.com/th/id/OIP.Ic4fs6C6iJ5UXHDIlQCkmgHaE8?w=240&h=180&c=7&r=0&o=5&pid=1.7')
    def __str__(self):
        return self.name + ' - ' + str(self.price) + ' - ' + self.hotel.name