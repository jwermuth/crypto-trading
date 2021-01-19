import os
import threading
import time
from pprint import pformat

import pandas as pd
from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor

from main.singleton import Singleton


class TradePairs:
    """Trade pair constants, makes it less likely not to misspell"""
    ETHBUSD = 'ETHBUSD'
    BTCUSDT = 'BTCUSDT'
    ETHUSDT = 'ETHUSDT'


class GetAssetBalances:
    """Show balances to operator, and try out python threads to get some performance"""
    def __init__(self):
        self.client = BinanceClient().client
        self._lock = threading.Lock()
        self._printable = ""

    def _get_asset_balance(self, asset):
        result = self.client.get_asset_balance(asset=asset)
        with self._lock:
            self._printable += "%-4s %f\n" % (result['asset'], float(result['free']))

    def print_asset_balances(self, assets):
        threads = []
        for asset in assets:
            t = threading.Thread(target=self._get_asset_balance, args=(asset,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        print(self._printable)


class Order:
    """Make an order, help with timeouts and other boilerplate stuff"""
    def __init__(self, timeout=10, order=None):
        self._timeout = timeout
        self.order = order
        self.client = BinanceClient().client

    def see_if_it_is_filled(self):
        order = self.client.get_order(symbol=self.order['symbol'], orderId=self.order['orderId'])
        waited = 0
        while order['status'] != self.client.ORDER_STATUS_FILLED and waited < self._timeout:
            # print(pformat(order))
            print("Order status: %s" % order['status'])
            time.sleep(1)
            waited += 1

        if waited >= self._timeout:
            print('waited to long. Cancelling')
            cancel = self.client.cancel_order(symbol=self.order['symbol'], orderId=self.order['orderId'])
            print(pformat(cancel))
            # TODO wait nicely to see the order actually cancel


class BinanceClient(metaclass=Singleton):
    """Single access point for binance client. Make it easier to split out more functionality"""
    def __init__(self):
        """Initialize Binance client"""
        print("init BinanceClient")
        api_key = os.environ.get('binance_api')
        api_secret = os.environ.get('binance_secret')

        self.client = Client(api_key, api_secret)
        self.client.API_URL = 'https://testnet.binance.vision/api'


class Prices(metaclass=Singleton):
    """give access to prices in a centralized place, with pandas for analysis"""
    def __init__(self):
        print("init PandaPrices")
        self._init_datastructures()

    def _init_datastructures(self):
        self._bsm_started = False
        # Keep historical prices, and allow to get prices whenever you want
        self.price = {'error': False}
        # Allow multiple user callbacks for each trade_pair. {'ETHBUSD': [cb, cb, ...]}
        self._user_callbacks = {}
        # Keep handles for easy retrieval
        self._handles = {}
        self.bsm = BinanceSocketManager(BinanceClient().client)

    def _my_callback(self, trade_pair):
        """define how to process incoming WebSocket messages"""
        def symbol_ticker_callback(msg):
            if msg['e'] != 'error':
                self.price[trade_pair].loc[len(self.price[trade_pair])] = [pd.Timestamp.now(), float(msg['c'])]
            else:
                self.price['error']: True
                # TODO Handle the error and restart socket
                #        if self.price['error']:
                #            # stop and restart socket
                #            self.bsm.stop_socket(symbol_ticker_ETHBUSD_handle)
                #            self.bsm.start()
                #            self.price['error'] = False
            if trade_pair in self._user_callbacks:
                for user_callback in self._user_callbacks[trade_pair]:
                    user_callback(msg)

        return symbol_ticker_callback

    def stop(self):
        """Stop websocket and all callbacks. This can only be called once, and PandaPrices can not be called again
        afterwards"""
        print("Stop websocket using connection key")
        for handle in self._handles:
            if not Prices().bsm.stop_socket(handle):
                # Try again
                Prices().bsm.stop_socket(handle)
        print("Properly terminate WebSocket.")
        reactor.stop()

    def add_trade_pair(self, trade_pair, user_callback):
        # If the trade pair is already present
        if trade_pair in self._handles:
            # the handle will be returned at the end of the function
            pass
        # Otherwise, its a new trade pair, some setup needs doing
        else:
            self.price[trade_pair] = pd.DataFrame(columns=['date', 'price'])
            symbol_ticker_handle = self.bsm.start_symbol_ticker_socket(trade_pair, self._my_callback(trade_pair))
            if not self._bsm_started:
                self.bsm.start()
                self._bsm_started = True

            # Print a little status, to avoid drowning the console
            count = 0
            while len(self.price[trade_pair]) == 0:
                count += 1
                if count == 1 or count % 50 == 0:
                    print("Waiting for %s ticker to start streaming data. This normally takes less than 10 seconds" % trade_pair)
                time.sleep(0.1)
            print("%s ticker is streaming data" % trade_pair)
            self._handles[trade_pair] = symbol_ticker_handle
            self._user_callbacks[trade_pair] = set()
        # The datatype set will allow any number of callbacks, pr. trade pair
        if user_callback:
            self._user_callbacks[trade_pair].add(user_callback)
        return self._handles[trade_pair]

    def last_price(self, trade_pair):
        try:
            if trade_pair not in self.price:
                return BinanceClient().client.get_symbol_ticker(symbol=trade_pair)['price']
            else:
                return self.price[trade_pair].iloc[-1].price
        except Exception as e:
            # TODO Error handling
            print(e)

