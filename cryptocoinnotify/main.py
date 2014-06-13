# -*- coding: utf-8 -*-
import logging
import multiprocessing
from cryptocoinnotify.backends import BACKENDS
from cryptocoinnotify.config import config


logging.basicConfig(level=logging.DEBUG if config.getboolean('main', 'debug') else logging.WARNING)

logger = logging.getLogger('cryptocoinnotify')


def proccess(backend):
    """:type: cryptocoinnotify.core.APIConnector"""
    logger.info("Start proccessing {0}".format(backend.name))
    pairs = ''
    if config.has_section(backend.name) and config.has_option(backend.name, 'currency_pairs'):
        pairs = config.get(backend.name, 'currency_pairs')

    if config.get('main', 'currency_pairs'):
        pairs += ' ' + config.get('main', 'currency_pairs')

    pairs = pairs.strip()
    pairs = [pair for pair in pairs.split(' ')]
    for pair in pairs:
        b = backend(pair)
        logger.info('Check pair {0}'.format(pair))
        b.process()


def main():
    proc_count = len(BACKENDS)
    pool = multiprocessing.Pool(proc_count)
    for b in BACKENDS:
        pool.apply_async(proccess, (b,))
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()