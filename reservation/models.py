# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from habitacion.models import Room

from django.utils import timezone

class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    main_customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_customer_reservations', null=False, blank=False)  
    customers = models.ManyToManyField(User, related_name='customer_reservations', blank=True)
    init_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Verificar si ya existe una reserva para esta habitación en el mismo rango de fechas
        reservas_existente = Reservation.objects.filter(room=self.room, init_date__lte=self.end_date, end_date__gte=self.init_date).exclude(pk=self.pk)
        if reservas_existente.exists():
            raise ValidationError('Esta habitación ya está reservada para estas fechas')

        # Si no hay reservas existentes, guardar la reserva
        super().save(*args, **kwargs)

