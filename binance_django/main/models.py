import typing
from django.db import models
from pprint import pformat


class GetAccount(models.Model):
    data = models.JSONField(null=True)

    def __str__(self):
        return "get_account %i" % self.pk

    def pformat_data(self):
        return pformat(self.data)


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


class CreateOrder(models.Model):
    """
    See also https://python-binance.readthedocs.io/en/latest/account.html#id2

    Get data for:
    order = client.create_order(
    symbol='BNBBTC',
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=100,
    price='0.00001')

    """
    symbol = models.CharField(max_length=6)
    # See https://docs.djangoproject.com/en/3.1/topics/db/models/
    side = models.TextChoices('Side', 'BUY')
    type = models.TextChoices('Type', 'LIMIT')
    timeInForce = models.TextChoices('timeInForce', 'GTC')
    quantity = models.FloatField()
    price = models.FloatField()


