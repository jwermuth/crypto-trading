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
        rv, created = Account.objects.get_or_create(
            makerCommission=dictionary['makerCommission'],
            takerCommission=dictionary['takerCommission'],
            buyerCommission=dictionary['buyerCommission'],
            sellerCommission=dictionary['sellerCommission'],
            canTrade=dictionary['canTrade'],
            canWithdraw=dictionary['canWithdraw'],
            canDeposit=dictionary['canDeposit'],
            updateTime=dictionary['updateTime'],
            accountType=dictionary['accountType'], )

        if 'balances' in dictionary:
            for balance in dictionary['balances']:
                rv.balances.get_or_create(
                    asset=balance['asset'],
                    free=balance['free'],
                    locked=balance['locked'], )
        if 'permissions' in dictionary:
            for permission in dictionary['permissions']:
                rv.permissions.get_or_create(permission=permission)
        return rv

    factory = staticmethod(factory)


class Balance(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='balances')
    asset = models.CharField(max_length=10)
    free = models.FloatField()
    locked = models.FloatField()


class Permission(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='permissions')
    permission = models.CharField(max_length=20)
