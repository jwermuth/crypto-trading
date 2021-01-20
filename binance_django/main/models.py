from django.db import models


# Create your models here.
class Account(models.Model):
    pass


class Balance(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    asset = models.CharField(max_length=10)
    free = models.FloatField()
    locked = models.FloatField()
