# -*- coding: utf-8 -*-
import decimal
import logging
import time

import requests

from cryptocoinnotify.config import config
from cryptocoinnotify.notify import NOTIFIERS
from cryptocoinnotify.storage import db


class ConfigurationError(Exception):
    pass


class APIGetter(object):
    pair = None

    @staticmethod
    def _average(lst):
        return float(decimal.Decimal(
            reduce(lambda x, y: decimal.Decimal(y) + decimal.Decimal(x), lst)
        ) / decimal.Decimal(len(lst)))

    def get_data_by_coin_exchange(self):
        return self._get_data_by_coin_exchange()

    def _get_data_by_coin_exchange(self):
        raise NotImplementedError()

    def last_price(self):
        return self._last_price()

    def _last_price(self):
        raise NotImplementedError()


class APIConnector(APIGetter):
    name = None
    base_url = None
    base_refresh_rate = 60  # Interval of data update on server
    cache = None
    interval = 24

    def __init__(self, pair):
        if not self.base_url:
            raise ConfigurationError()

        self.pair = pair
        self.coins = [v.strip() for v in pair.strip().split('-')]
        self.cache = {}
        self.logger = logging.getLogger('cryptocoinnotify.backend.{0}'.format(self.name))

        enabled_notifiers = config.get('notify', 'enabled')
        notifiers = [v.strip() for v in enabled_notifiers.split(',')]
        self.notifiers = [v for k, v in NOTIFIERS.items() if k in notifiers]

        super(APIConnector, self).__init__()

    def _call(self, *args, **kwargs):
        key = ''.join(args) + ''.join(['%s%s' % (k, v) for k, v in kwargs.items()])
        if key in self.cache:
            return self.cache[key]

        url = self._build_url(*args, **kwargs)
        res = requests.get(url)
        if res.status_code != 200:
            self.logger.warning(
                'Wrong status code response {0}, while accessing {1}'.format(res.status_code, url)
            )
            return None
        else:
            self.logger.debug('Url {0} accessed successfully'.format(url))
            r = res.json()
            self.cache[key] = r
            return r

    def log(self, value, pair):
        if float(value) == 0.0:
            return 0, 0, 0, 0

        log = self._get_log(pair)
        last = [decimal.Decimal(v[4]) for v in log]
        if len(last) == self.interval * 60 * self.base_refresh_rate:
            last.pop(0)

        last.append(value)
        average = round(self._average(last), 8)
        if len(log) > 0:
            last_average = log[len(log) - 1][3]
            last_value = log[len(log) - 1][4]
        else:
            last_average = 0
            last_value = 0

        now = time.time()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO log (server, timestamp, value, average, pair) VALUES (?, ?, ?, ?, ?)",
            (self.name, now, value, average, pair)
        )
        db.commit()
        return value, average, last_average, last_value

    def _get_log(self, pair):
        min_time = time.time() - self.interval * 60 * 60
        cursor = db.cursor()
        rows = cursor.execute(
            "SELECT * FROM log WHERE server=? AND timestamp >= ? AND pair=? "
            "ORDER BY timestamp ASC",
            (self.name, min_time, pair)
        ).fetchall()
        return rows

    def _get_log_last(self, pair):
        min_time = time.time() - self.interval * 60 * 60
        cursor = db.cursor()
        row = cursor.execute(
            "SELECT * FROM log WHERE server=? AND timestamp >= ? AND pair=?"
            " ORDER BY timestamp DESC LIMIT 1",
            (self.name, min_time, pair)
        ).fetchone()
        return row

    def _build_url(self, *args, **kwargs):
        raise NotImplementedError()

    def process(self):
        lp = self.last_price()
        value, average, last_average, last_value = self.log(lp, self.pair)
        if value == 0:
            return 0

        percent = config.getfloat('main', 'delta_percent')
        if config.has_option(self.name, 'delta_percent'):
            percent = config.getfloat(self.name, 'delta_percent')

        p = 100 - last_average / average * 100.0

        if abs(p) > percent:
            self.notify(average, last_average, value, last_value, p)

        return average

    def notify(self, average, last_average, value, last_value, percents):
        if last_value > 0 and last_average > 0:
            message = config.get('notify', 'notification_text').format(
                pair=self.pair, server=self.name, percent=percents,
                average=average, last_average=last_average, value=value,
                last_value=last_value)
            print message
            for notifier in self.notifiers:
                print notifier
                m = notifier(message)
                m.send()
