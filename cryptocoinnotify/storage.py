# -*- coding: utf-8 -*-
import sqlite3
import sys

import psycopg2

from cryptocoinnotify.config import config


db = sqlite3.connect(config.get('DB', 'db_path'))

cursor = db.cursor()
try:
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY AUTOINCREMENT, server TEXT,'
        'timestamp INTEGER, average REAL, value NUMERIC, pair TEXT)'
    )
except Exception as e:
    print "Failed to create tables. {0}".format(e.message)
    sys.exit(104)


class Storage(object):
    def __init__(self):
        pass

    def _insert(self, **kwargs):
        raise NotImplementedError()

    def _select(self, **kwargs):
        raise NotImplementedError()

    def _create_tables(self):
        raise NotImplementedError()


class PostgresStorage(Storage):
    def __init__(self):
        self.conn = psycopg2.connect(database='cryptocoinnotify', user='user', password='password')
        super(PostgresStorage, self).__init__()

    def _insert(self, **kwargs):
        table = kwargs.pop('table')
        fields = ",".join([k for k in kwargs.keys()])
        values = ",".join(['%s' % v for v in kwargs.values()])
        sql = "INSERT INTO {TABLE} ({fields}) VALUES ({VALUES})".format(
            table=table, fields=fields, values=values
        )
        c = self.conn.cursor()
        c.execute(sql)
        return c

    def _select(self, **kwargs):
        table = kwargs.pop('table')
        limit = kwargs.pop('limit', None)
        offset = kwargs.pop('offset', 0)
        if limit:
            limit = "LIMIT {0} OFFSET {1}".format(limit, offset)
        else:
            limit = ''

        fields = kwargs.pop('fields', "*")
        raw_where = kwargs.pop('raw_where', None)
        where = " AND ".join(["%s=%s" % (k, v) for k, v in kwargs.items()])
        where += raw_where

        sql = "SELECT {fields} FROM {TABLE} WHERE {WHERE} {LIMIT}".format(
            fields=fields, table=table, where=where, limit=limit
        )

        c = self.conn.cursor()
        c.execute(sql)
        return c

    def _create_tables(self):
        sql = """
          CREATE TABLE IF NOT EXISTS log (
            id INTEGER auto_increment NOT NULL PRIMARY KEY,
            server VARCHAR(40) NOT NULL
          )
        """

        c = self.conn.cursor()
        c.execute(sql)