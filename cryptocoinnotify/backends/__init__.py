# -*- coding: utf-8 -*-
from cryptocoinnotify.backends.bittrex import BittrexAPI
from cryptocoinnotify.backends.cryptsy import CryptsyApi
from cryptocoinnotify.backends.mintpal import MintpalAPI
from cryptocoinnotify.backends.poloniex import PoloniexAPI

BACKENDS = [BittrexAPI, CryptsyApi, MintpalAPI, PoloniexAPI]