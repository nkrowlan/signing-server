from twisted.internet import defer

class SayHiImplementation(object):
    """
    Responds with 'hello, %s' % arg
    """
    def say_hi(self, identifier):
        d = defer.Deferred()
        d.callback('hello, %s' % identifier)
        return d
