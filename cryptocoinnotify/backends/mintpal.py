# -*- coding: utf-8 -*-
from cryptocoinnotify.core import APIConnector


class MintpalAPI(APIConnector):
    """
    >>> a = MintpalAPI('AUR-BTC')
    >>> res = a.get_data_by_coin_exchange()
    >>> print len(res)
    1
    >>> print res[0]['code']
    AUR
    >>> res = a.last_price()
    >>> print float(res) > 0
    True
    """
    name = 'mintpal'
    base_url = 'https://api.mintpal.com/v1/market'

    def _build_url(self, *args, **kwargs):
        url = "{0}/{1}".format(
            self.base_url, '/'.join(args)
        )
        return url

    def _get_data_by_coin_exchange(self):
        return self._call('stats', self.coins[0], self.coins[1])

    def _last_price(self):
        return self.get_data_by_coin_exchange()[0]['last_price']