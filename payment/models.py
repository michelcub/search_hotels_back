from django.db import models
from reservation.models import Reservation
# Create your models here.
class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    def __str__(self):
        return str(self.amount) + ' - ' + str(self.created_at)