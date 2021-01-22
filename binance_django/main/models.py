import typing
from django.db import models


class Account(models.Model):
    makerCommission = models.FloatField()
    takerCommission = models.FloatField()
    buyerCommission = models.FloatField()
    sellerCommission = models.FloatField()
    canTrade = models.BooleanField()
    canWithdraw = models.BooleanField()
    canDeposit = models.BooleanField()
    updateTime = models.PositiveBigIntegerField()
    accountType = models.CharField(max_length=20, )

    def __str__(self):
        return "%s" % self.__dict__

    def factory(dictionary):
        rv = Account()
        rv.makerCommission = dictionary['makerCommission']
        rv.takerCommission = dictionary['takerCommission']
        rv.buyerCommission = dictionary['buyerCommission']
        rv.sellerCommission = dictionary['sellerCommission']
        rv.canTrade = dictionary['canTrade']
        rv.canWithdraw = dictionary['canWithdraw']
        rv.canDeposit = dictionary['canDeposit']
        rv.updateTime = dictionary['updateTime']
        rv.accountType = dictionary['accountType']
        return rv

    factory = staticmethod(factory)


class Balance(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='balances')
    asset = models.CharField(max_length=10)
    free = models.FloatField()
    locked = models.FloatField()

    def __init__(self, *args, response: typing.Any = None, **kwargs):
        super().__init__(*args, **kwargs)
        if response is not None:
            self.__dict__.update(response)

# class Permission(models.Model):
#    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='permissions')
#    permission = models.CharField(max_length=20)
#
#    def __init__(self, *args, response: typing.Any=None, **kwargs):
#        super().__init__(*args, **kwargs)
#        if response is not None:
#            self.__dict__.update(response)
#
