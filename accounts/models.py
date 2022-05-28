from django.db import models

class Userinfo(models.Model):
    username = models.CharField(max_length=150)
    balance = models.IntegerField(default=100)
    book = models.BooleanField(default=False)
    open_gate = models.BooleanField(default=False)
    inside_gate = models.BooleanField(default=False)

class Parking_history(models.Model):
    user_name = models.CharField(max_length=150)
    in_time = models.DateTimeField()
    out_time = models.DateTimeField()
    avilable = models.IntegerField()
    filled = models.IntegerField()
    booking_time = models.DateTimeField()

class Balance_history(models.Model):
    user_name = models.CharField(max_length=150)
    balance_time = models.DateTimeField()
    owner_earning = models.IntegerField()
    balance_added = models.IntegerField()