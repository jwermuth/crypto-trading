from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from main.models import Account

a = {
    'makerCommission': 1,
    'takerCommission': 2,
    'buyerCommission': 3,
    'sellerCommission': 4,
    'canTrade': True,
    'canWithdraw': True,
    'canDeposit': True,
    'updateTime': 243234432,
    'accountType': 'SPOT',
    'balances': [
        {
            'asset': 'BNB',
            'free': '1000.00000000',
            'locked': '0.00000000'
        },
        {
            'asset': 'ETH',
            'free': '105.00000000',
            'locked': '3.00000000'
        },
    ],
    'permissions': [
        'SPOT'
    ]
}


class AccountModelTest(TestCase):
    def test_create_with_factory_deep(self):
        """
        Create a model object with nested objects.
        """
        account = Account.factory(a)
        account.save()

        self.assertEqual(account.makerCommission, 1)
        self.assertEquals(account.balances.all().filter(asset='BNB').get().free, 1000)
        self.assertEquals(account.balances.all().filter(asset='ETH').get().free, 105)


class MainIndexViewTests(TestCase):
    def test_is_present(self):
        """
        Something responds at the index url
        """
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)


class GetAccountViewTests(TestCase):
    def test_is_present(self):
        """
        Something responds at the index url
        """
        response = self.client.get(reverse('main:get_account'))
        self.assertEqual(response.status_code, 200)
