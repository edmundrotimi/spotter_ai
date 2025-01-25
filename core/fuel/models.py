from django.db import models
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField


class FuelPrices(models.Model):
    id = ShortUUIDField(length=30, max_length=40, alphabet='16777216', primary_key=True)  # noqa: A003
    opis_id = models.IntegerField(verbose_name='OPIS Id')
    truckstop_name = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    state = models.CharField(max_length=500, null=True, blank=True)
    rack_id = models.IntegerField(verbose_name='Rack Id')
    retail_price = models.FloatField()
    creation_time = models.DateField(auto_now_add=True)
    last_update = models.DateTimeField(default=timezone.now, help_text='time last updated')

    def __str__(self):
        return f'OPIS Id: {self.opis_id}'

    class Meta:
        verbose_name = 'Fuel Price'
        verbose_name_plural = 'Fuel Prices'
