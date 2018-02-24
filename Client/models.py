# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CurrencyCode(BaseModel):
    currency_name = models.CharField(max_length=128)
    currency_code = models.CharField(max_length=12)
    
    def __unicode__(self):
        return self.currency_name
    

class ExpensesTracker(BaseModel):
    expensed_on = models.DateTimeField()
    title = models.CharField(max_length=256)
    amount = models.FloatField(null=True)
    description = models.CharField(max_length=1024)
    currency = models.ForeignKey(CurrencyCode,null=True)
    client = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title
    
class ExpenseProduct(BaseModel):
    product_name = models.CharField(max_length=128)
    product_type = models.CharField(max_length=64)
    quantity = models.IntegerField()
    cost = models.FloatField()
    expensetracker = models.ForeignKey(ExpensesTracker)
    