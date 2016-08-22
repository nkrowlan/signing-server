from twisted.internet import defer
from signing.processor import expose
from signing.persistence import Persistence

class StoreImplementation(object):
    def __init__(self):
        self.store = Persistence()

    """
    Responds with 'hello, %s' % arg
    """
    @expose
    def say_hi(self, key):
        d = defer.Deferred()
        d.callback('hello, %s' % key)
        return d

    @expose
    def set(self, key, field, value):
        return self.store.set(key, field, value).addCallback(lambda _: "set")

    @expose
    def get(self, key, field):
        return self.store.get(key, field)

    @expose
    def delete(self, key, field = None):
        return self.store.delete(key, field).addCallback(lambda _: "deleted")

    @expose
    def get_all(self, key):
        return self.store.get_all(key).addCallback(repr)
