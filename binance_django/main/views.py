from django.http import HttpResponse
from pprint import pformat
from main.binance_helpers import TradePairs, BinanceClient


def index(request):
    client = BinanceClient().client
    print(pformat(client.get_all_orders(symbol=TradePairs.ETHBUSD)))
    return HttpResponse(
        "Hello, world. You're at the main index. %s" % pformat(client.get_account()))
