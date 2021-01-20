from django.http import HttpResponse
from pprint import pformat
from .binance_helpers import BinanceClient, TradePairs
from django.template import loader


def index(request):
    client = BinanceClient().client
    print(pformat(client.get_all_orders(symbol=TradePairs.ETHBUSD)))
    return HttpResponse(
        "Hello, world. You're at the main index. %s" % pformat(client.get_account()))


def get_account(request):
    client = BinanceClient().client

    template = loader.get_template('main/get_account.html')
    account = client.get_account()
    context = {'json_response': pformat(account), 'account_info': account}
    return HttpResponse(template.render(context, request))
