from django.db import models

# Create your models here.
class Room(models.Model):
    number = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.TextField()
    hotel = models.ForeignKey('hotel.Hotel', on_delete=models.CASCADE)
    CATEGORY = (
        ('B', 'Basic'),
        ('C', 'Confort'),
        ('P', 'Premium'),
    )
    type = models.CharField(max_length=1, choices=CATEGORY)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.price: 
            self.price = self.calculate_price()
        super().save(*args, **kwargs)

    def calculate_price(self):
        if self.type == 'B':
            return 170.00
        elif self.type == 'C':
            return 220.00
        elif self.type == 'P':
            return 298.00
        else:
            return 0.00

    def __str__(self):
        return self.name