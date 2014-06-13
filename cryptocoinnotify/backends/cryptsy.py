# -*- coding: utf-8 -*-
from cryptocoinnotify.core import APIConnector


class CryptsyApi(APIConnector):
    """
    >>> a = CryptsyApi('LTC-BTC')
    >>> res = a.get_data_by_coin_exchange()
    >>> print bool(res)
    True
    >>> res = a.last_price()
    >>> print float(res) >= 0
    True
    """
    name = 'cryptsy'
    base_url = 'http://pubapi.cryptsy.com/api.php'
    market_codes = None

    def _get_market_code(self, coin, exchange):
        if not self.market_codes:
            self.market_codes = {}
            data = self._call('marketdatav2')
            markets = data['return']['markets']
            for market in markets.values():
                cs = "{0}-{1}".format(market['primarycode'], market['secondarycode'])
                self.market_codes[cs] = market['marketid']
        cs = "{0}-{1}".format(coin, exchange)
        return self.market_codes[cs]

    def _build_url(self, method, marketid=None, **kwargs):
        url = "{0}?method={1}".format(self.base_url, method)
        if marketid:
            url = "{0}&marketid={1}".format(url, marketid)
        return url

    def _get_data_by_coin_exchange(self):
        code = self._get_market_code(self.coins[0], self.coins[1])
        return self._call('singlemarketdata', code)['return']['markets'][self.coins[0]]

    def _last_price(self):
        return self.get_data_by_coin_exchange()['lasttradeprice']