# -*- coding: utf-8 -*-
from cryptocoinnotify.core import APIConnector


class PoloniexAPI(APIConnector):
    """
    >>> a = PoloniexAPI('BTC-NXT')
    >>> print bool(a.get_data_by_coin_exchange())
    True
    >>> print float(a.last_price()) > 0
    True
    >>> print bool(a.process())
    True
    """
    name = 'poloniex'
    base_url = 'https://poloniex.com/public'

    def _build_url(self, command, **kwargs):
        url = "{0}?command={1}&{2}".format(
            self.base_url, command,
            '&'.join(['%s=%s' % (self.coins[0], self.coins[1])])
        )
        return url

    def _get_data_by_coin_exchange(self):
        currencypair = "{0}_{1}".format(self.coins[0], self.coins[1])
        return self._call('returnTicker')[currencypair]

    def _last_price(self):
        return self.get_data_by_coin_exchange()['last']