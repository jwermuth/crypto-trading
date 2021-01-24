from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from pprint import pformat
from .binance_helpers import BinanceClient, TradePairs
from django.template import loader
from .models import Balance, Account, GetAccount
import json
from ast import literal_eval
import pickle


def index(request):
    template = loader.get_template('main/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def get_account(request):
    client = BinanceClient().client

    template = loader.get_template('main/get_account.html')
    account = client.get_account()

#    last = Account.objects.last()
#    if last is not None and last.updateTime != account.updateTime:
#        new_account = Account(
#            makerCommission=account['makerCommission'],
#            takerCommission=account['takerCommission'],
#            buyerCommission=account['buyerCommission'],
#            sellerCommission=account['sellerCommission'],
#            canTrade=account['canTrade'],
#            canWithdraw=account['canWithdraw'],
#            canDeposit=account['canDeposit'],
#            updateTime=account['updateTime'])
#        for balance in account.balances:

    context = {'json_response': str(account), 'account': account}
    return HttpResponse(template.render(context, request))


def get_access_balance(request, asset):
    client = BinanceClient().client

    template = loader.get_template('main/get_asset_balance.html')
    response = client.get_asset_balance(asset=asset)
    print(response)
    context = {'json_response': pformat(response), 'response': response}
    return HttpResponse(template.render(context, request))


def save_account(request):
    print("save_account")
    account = request.POST['account']


    print(account)
    print(type(account))

    #    account_info = pickle.loads(account_info)
    account = literal_eval(account)
    print(account)
    print(type(account))

    # Also save as json to experiment with json later.
    GetAccount.objects.create(data=account)


    account_model = Account.factory(account)
    print(account_model)
    print(account_model.makerCommission)

    print("Saving account")
    account_model.save()
    print("Saved")
    return HttpResponseRedirect(reverse('main:get_account'))
