# -*- coding: utf-8 -*-
import ConfigParser
import os
import sys

prefix = getattr(sys, "prefix")
if prefix == '/usr':
    prefix = ''

config = ConfigParser.ConfigParser(
    defaults={'DEBUG': 'False', 'db_path': '/var/tmp/database.sqlite3'},
    allow_no_value=True
)
config.read(
    [
        os.path.dirname(__file__) + '/cryptocoinnotify.cfg',
        prefix + '/etc/cryptocoinnotify.cfg',
        os.path.join(
            os.path.expanduser("~"), '.config', 'cryptocoinnotify.cfg'
        ),
    ]
)
