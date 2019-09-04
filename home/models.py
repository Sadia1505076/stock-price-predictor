from django.db import models
from django.db.models import BigIntegerField


class Company(models.Model):
    trade_code = models.CharField(max_length=50, primary_key=True, null=False)
    company_name = models.CharField(max_length=100, null=True)
    authorized_capital = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    paid_up_capital = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    outstanding_share_number = BigIntegerField(null=True, blank=True)
    sector = models.CharField(max_length=45, null=True, blank=True)


class SharePrediction(models.Model):
    class Meta:
        unique_together = (('trade_code', 'date'),)
    trade_code = models.CharField(max_length=50, null=False, blank=False)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, null=False)
    future_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=None)


class DSEHistory(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False, null=False, primary_key=True)
    dsex_index = models.DecimalField(max_digits=13, decimal_places=3, null=True, blank=True)
    total_trade = BigIntegerField(null=True, blank=True)
    total_volume = BigIntegerField(null=True, blank=True)
    total_value = models.DecimalField(max_digits=13, decimal_places=3, null=True, blank=True)
    total_market_cap = models.DecimalField(max_digits=13, decimal_places=3, null=True, blank=True)


class DSEPrediction(models.Model):
    date = models.DateTimeField(auto_now=False, auto_now_add=False, null=False, primary_key=True)
    future_index = models.DecimalField(max_digits=13, decimal_places=3, null=True, blank=True)


class ShareHistory(models.Model):
    class Meta:
        unique_together = (('trade_code', 'date'),)

    trade_code = models.CharField(max_length=50, null=False, blank=False)
    date = models.DateTimeField(auto_now=False, auto_now_add=False, null=False)
    opening_price = models.DecimalField(max_digits=13, decimal_places=3, null=True, blank=True)
    max_price = models.DecimalField(max_digits=13, decimal_places=3, null=True, blank=True)
    min_price = models.DecimalField(max_digits=13, decimal_places=3, null=True, blank=True)
    closing_price = models.DecimalField(max_digits=13, decimal_places=3, null=True, blank=True)
    total_volume = BigIntegerField(null=True, blank=True)

