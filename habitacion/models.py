from django.db import models


class RoomType(models.Model):
    hotel = models.ForeignKey('hotel.Hotel', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    max_customers = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return self.name

# Create your models here.
class Room(models.Model):
    number = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.TextField()
    hotel = models.ForeignKey('hotel.Hotel', on_delete=models.CASCADE)
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_customers = models.IntegerField(default=1, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.price: 
            self.calculate_price()
            self.set_max_customers()
            self.set_description()
            
        super().save(*args, **kwargs)

    def calculate_price(self):
        self.price = self.type.price
    
    def set_max_customers(self):
        self.max_customers = self.type.max_customers
    
    def set_description(self):
        self.description = self.type.description    
    

    def is_available(self, init_date, end_date):
        from reservation.models import Reservation
        return not Reservation.objects.filter(room=self, init_date__lte=end_date, end_date__gte=init_date).exists()
        
    def __str__(self):
        return self.number + ' - ' + self.hotel.name + ' - ' + self.type.name + ' - ' + str(self.price)