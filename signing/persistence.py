# -*- test-case-name: signing.test.test_persistence -*-

from twisted.internet import defer

class Persistence(object):
    """
    Simple deferred key:(field:value) store.

    If a field is set which already has a value, the value is overwritten.

    get_all returns a list of all fields for that key.
    """
    keyvals = {}

    def set(self, key, field, value):
        d = defer.Deferred()

        if key not in self.keyvals:
            self.keyvals[key] = {}

        self.keyvals[key][field] = value

        d.callback(None)

        return d

    def get(self, key, field):
        d = defer.Deferred()

        if key not in self.keyvals:
            d.callback(None)
        elif field not in self.keyvals[key]:
            d.callback(None)
        else:
            d.callback(self.keyvals[key][field])

        return d

    def get_all(self, key):
        d = defer.Deferred()

        if key not in self.keyvals:
            d.callback([])
        else:
            d.callback(self.keyvals[key].keys())

        return d

    def delete(self, key, field = None):
        d = defer.Deferred()
        if key in self.keyvals:
            if field in self.keyvals[key]:
                del self.keyvals[key][field]

            if field is None or len(self.keyvals[key]) == 0:
                del self.keyvals[key]

        d.callback(None)

        return d
