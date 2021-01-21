from django.http import HttpResponse
from pprint import pformat
from .binance_helpers import BinanceClient, TradePairs
from django.template import loader
from .models import Balance, Account
#from collections import namedtuple


def index(request):
    template = loader.get_template('main/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def get_account(request):
    client = BinanceClient().client

    template = loader.get_template('main/get_account.html')
    account = client.get_account()
    print(account)
    #account = namedtuple("Account", account.keys())(*account.values())
    account = Account(account)
    print(type(account))
    print(account)
    print(type(account.balances.all()))
    for b in account.balances.all():
        print(type(b))
        print(b)

    context = {'json_response': pformat(account), 'account_info': account}
    return HttpResponse(template.render(context, request))
