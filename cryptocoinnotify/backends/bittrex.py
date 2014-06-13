# -*- coding: utf-8 -*-
from cryptocoinnotify.core import APIConnector


class BittrexAPI(APIConnector):
    """
    >>> a = BittrexAPI('BTC-LTC')
    >>> print bool(a.get_data_by_coin_exchange())
    True
    >>> print float(a.last_price()) > 0
    True
    """
    name = 'bittrex'
    base_url = 'https://bittrex.com/api/v1/public/'

    def _build_url(self, *args, **kwargs):
        url = "{0}/{1}?{2}".format(
            self.base_url, '/'.join(args),
            "&".join(
                ["{0}={1}".format(k, v) for k, v in kwargs.items()]
            )
        )
        return url

    def _get_data_by_coin_exchange(self):
        market = "{0}-{1}".format(self.coins[0], self.coins[1])
        return self._call('getticker', market=market)['result']

    def _last_price(self):
        return self.get_data_by_coin_exchange()['Last']