from twisted.trial import unittest

from signing.persistence import Persistence

class PersistenceTests(unittest.TestCase):
    def setUp(self):
        self.persistence = Persistence()

    def test_set_get(self):
        d = self.persistence.set('somekey', 'somefield', 'somevalue')
        d.addCallback(lambda _: self.persistence.get('somekey', 'somefield'))
        return d.addCallback(self.assertEquals, 'somevalue')

    def test_update(self):
        d = self.persistence.set('updatekey', 'updatefield', 'firstvalue')
        d.addCallback(lambda _: self.persistence.set('updatekey', 'updatefield', 'secondvalue'))
        d.addCallback(lambda _: self.persistence.get('updatekey', 'updatefield'))
        return d.addCallback(self.assertEquals, 'secondvalue')

    def test_delete(self):
        d = self.persistence.set('deletekey', 'deletefield', 'somevalue')
        d.addCallback(lambda _: self.persistence.delete('deletekey', 'deletefield'))
        d.addCallback(lambda _: self.persistence.get('deletekey', 'deletefield'))
        return d.addCallback(self.assertEquals, None)

    def test_getAll(self):
        d = self.persistence.set('getallkey', 'getallfield', 'getallvalue')
        d.addCallback(lambda _: self.persistence.set('getallkey', 'getallfield2', 'getallvalue2'))
        d.addCallback(lambda _: self.persistence.get_all('getallkey'))
        return d.addCallback(lambda result: self.assertTrue('getallfield' in result and 'getallfield2' in result))

    def test_deleteAll(self):
        d = self.persistence.set('deleteall_key', 'deleteall_field', 'deleteall_value')
        d.addCallback(lambda _: self.persistence.delete('deleteall_key'))
        d.addCallback(lambda _: self.persistence.get_all('deleteall_key'))
        return d.addCallback(self.assertEquals, [])
