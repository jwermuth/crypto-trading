import typing
from django.db import models


class Account(models.Model):
    makerCommission = models.FloatField(null=True)
    takerCommission = models.FloatField(null=True)
    buyerCommission = models.FloatField(null=True)
    sellerCommission = models.FloatField(null=True)
    canTrade = models.BooleanField(null=True)
    canWithdraw = models.BooleanField(null=True)
    canDeposit = models.BooleanField(null=True)
    updateTime = models.TimeField(null=True)
    accountType = models.CharField(max_length=20, null=True)

    def __init__(self, *args, response: typing.Any=None, **kwargs):
        super().__init__(*args, **kwargs)
        if response is not None:
            self.__dict__.update(response)


class Balance(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='balances')
    asset = models.CharField(max_length=10)
    free = models.FloatField()
    locked = models.FloatField()

    def __init__(self, *args, response: typing.Any=None, **kwargs):
        super().__init__(*args, **kwargs)
        if response is not None:
            self.__dict__.update(response)
