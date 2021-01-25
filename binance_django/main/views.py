from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from pprint import pformat
from .binance_helpers import BinanceClient, TradePairs
from django.template import loader
from .models import Balance, Account, GetAccount, CreateOrder
from ast import literal_eval
from django.views import generic
from binance.exceptions import BinanceAPIException, BinanceOrderException
from django.contrib import messages
from django.contrib import messages

def index(request):
    template = loader.get_template('main/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


# def get_account(request):
#     client = BinanceClient().client
#
#     template = loader.get_template('main/get_account.html')
#     account = client.get_account()
#
# #    last = Account.objects.last()
# #    if last is not None and last.updateTime != account.updateTime:
# #        new_account = Account(
# #            makerCommission=account['makerCommission'],
# #            takerCommission=account['takerCommission'],
# #            buyerCommission=account['buyerCommission'],
# #            sellerCommission=account['sellerCommission'],
# #            canTrade=account['canTrade'],
# #            canWithdraw=account['canWithdraw'],
# #            canDeposit=account['canDeposit'],
# #            updateTime=account['updateTime'])
# #        for balance in account.balances:
#
#     context = {'json_response': str(account), 'account': account}
#     return HttpResponse(template.render(context, request))
#
#
# def get_access_balance(request, asset):
#     client = BinanceClient().client
#
#     template = loader.get_template('main/get_asset_balance.html')
#     response = client.get_asset_balance(asset=asset)
#     print(response)
#     context = {'json_response': pformat(response), 'response': response}
#     return HttpResponse(template.render(context, request))
#
#
# def save_account(request):
#     print("save_account")
#     account = request.POST['account']
#
#
#     print(account)
#     print(type(account))
#
#     #    account_info = pickle.loads(account_info)
#     account = literal_eval(account)
#     print(account)
#     print(type(account))
#
#     # Also save as json to experiment with json later.
#     GetAccount.objects.create(data=account)
#
#
#     account_model = Account.factory(account)
#     print(account_model)
#     print(account_model.makerCommission)
#
#     print("Saving account")
#     account_model.save()
#     print("Saved")
#     return HttpResponseRedirect(reverse('main:get_account'))


class IndexView(generic.ListView):
    def get_queryset(self):
        """ return all saved get_account calls"""
        return GetAccount.objects.all()


class DetailView(generic.DetailView):
    model = GetAccount


def get_all_orders_tradepair(request, tradepair):
    template = loader.get_template('main/get_all_orders_tradepair.html')
    client = BinanceClient().client
    orders = client.get_all_orders(symbol=tradepair)
    context = {'orders': orders}
    return HttpResponse(template.render(context, request))


class IndexView(generic.ListView):
    def get_queryset(self):
        return CreateOrder.objects.all()


class DetailView(generic.DetailView):
    model = CreateOrder


def create_order(request):
    print('create order')
    template = loader.get_template('main/create_order.html')
    context = {}
    order_reference = None
    if request.method == 'POST':
        context['error_message'] = 'no errors'
        # Your code for POST
        typea = request.POST['typea']
        symbol = request.POST['symbol']
        side = request.POST['side']
        time_in_force = request.POST['timeInForce']
        quantity = request.POST['quantity']
        price = request.POST['price']

        try:
            order_reference = BinanceClient().client.create_order(
                symbol=symbol,
                side=side,
                type=typea,
                timeInForce=time_in_force,
                quantity=quantity,
                price=price)
            context['message'] = 'Created order %s. Create another ?' % order_reference
        except BinanceAPIException as e:
            # error handling goes here
            context['error_message'] = e.message
            print(e)
        except BinanceOrderException as e:
            context['error_message'] = e.message
            # error handling goes here
            print(e)

    else:
        context['message'] = 'Create an order'
        context['error_message'] = 'no errors'
    return HttpResponse(template.render(context, request))


def get_account(request):
    client = BinanceClient().client

    template = loader.get_template('main/get_account.html')
    account = client.get_account()

    context = {'json_response': pformat(account), 'account': account}
    return HttpResponse(template.render(context, request))


def api(request):
    template = loader.get_template('main/api.html')
    return HttpResponse(template.render({}, request))


def get_all_orders(request, symbol):
    context = {}
    try:
        orders = BinanceClient().client.get_all_orders(symbol=symbol, limit=10)
        context['dict_response'] = orders
    except BinanceAPIException as e:
        messages.error(request, e.message)
        print(e)
    except BinanceOrderException as e:
        messages.error(request, e.message)
        print(e)

    template = loader.get_template('main/order_list.html')
    return HttpResponse(template.render(context, request))


def get_open_orders(request, symbol):
    context = {}
    try:
        orders = BinanceClient().client.get_open_orders(symbol=symbol)
        context['dict_response'] = orders
    except BinanceAPIException as e:
        messages.error(request, e.message)
        print(e)
    except BinanceOrderException as e:
        messages.error(request, e.message)
        print(e)

    template = loader.get_template('main/order_list.html')
    return HttpResponse(template.render(context, request))


def cancel_order(request, symbol, order_id):
    print("cancel_order")
    context = {}
    try:
        dict_response = BinanceClient().client.cancel_order(symbol=symbol, orderId=order_id)
        print('asked api')
        context['dict_response'] = dict_response
    except BinanceAPIException as e:
        # error handling goes here
        messages.error(request, e.message)
        print(e)
    except BinanceOrderException as e:
        messages.error(request, e.message)
        # error handling goes here
        print(e)

    return HttpResponseRedirect(reverse('main:get_all_orders', args=[symbol]))
