import unittest
from cryptocoinnotify.backends import BACKENDS

from cryptocoinnotify.storage import db


class TestBackends(unittest.TestCase):
    def test_backends_list(self):
        lst = BACKENDS
        self.assertTrue(lst)
        module = lst[0]('BTC-LTC')
        module.process()


class TestStorage(unittest.TestCase):
    def test_db_init(self):
        cursor = db.cursor()
        self.assertTrue(cursor.execute('CREATE TABLE TEST (id INT)'))
        cursor.execute('INSERT INTO TEST (id) VALUES (1)')
        db.commit()
        r = cursor.execute('SELECT * FROM TEST').fetchone()
        self.assertEquals(r, (1,))
        self.assertTrue(cursor.execute('DROP TABLE TEST'))


if __name__ == '__main__':
    unittest.main()
