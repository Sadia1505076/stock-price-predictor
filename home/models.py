
from django.db import models
from django.db.models import BigIntegerField


class Company(models.Model):
    trade_code = models.CharField(max_length=50, primary_key=True, null=False)
    company_name = models.CharField(max_length=100, null=True)
    authorized_capital = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    paid_up_capital = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    outstanding_share_number = BigIntegerField(null=True, blank=True)
    sector = models.CharField(max_length=45, null=True, blank=True)


