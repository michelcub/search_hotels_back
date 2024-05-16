# Create your models here.
import random
import string
from django.db import models
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from habitacion.models import Room
from hotel.models import Hotel, Services

from django.utils import timezone

class Reservation(models.Model):
    locator = models.CharField(max_length=6, unique=True, null=True, blank=True)
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE , related_name='hotel_reservations', null=True, blank=True, )
    services = models.ManyToManyField(Services, related_name='reservation_services', blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    main_customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_customer_reservations', null=False, blank=False)  
    customers = models.ManyToManyField(User, related_name='customer_reservations', blank=True)
    init_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, default=None)
    
    
    is_paid = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        reservas_existente = Reservation.objects.filter(room=self.room, init_date__lte=self.end_date, end_date__gte=self.init_date).exclude(pk=self.pk)
        if reservas_existente.exists():
            raise ValidationError('Esta habitación ya está reservada para estas fechas')
        if not self.locator:
            self.locator = self.generate_locator()
        super().save(*args, **kwargs)

    def calculate_amount(self):
        days = (self.end_date - self.init_date).days
        amount_total_days = self.room.price * days
        amount_services = sum([service.price for service in self.services.all()])
        self.amount = amount_total_days + amount_services
        
        self.save() 
        
    def generate_locator(self):
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choices(characters, k=6))
        
    def check_is_paid(self):
        from payment.models import Payment
        amount_paid = Payment.objects.filter(reservation=self).aggregate(models.Sum('amount'))['amount__sum']
        if amount_paid is not None and amount_paid >= self.amount:
            self.is_paid = True
        else:
            self.is_paid = False
        self.save()

        
    def __str__(self):
        return f'{self.room.number} - {self.init_date} - {self.end_date}'