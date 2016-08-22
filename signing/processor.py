# -*- test-case-name: signing.test.test_processor -*-

from twisted.internet import defer
from twisted.python import log

class NoSuchCommand(Exception):
    pass

class WrongNumberOfArguments(Exception):
    pass

_cmds = []

def expose(f):
    if f in _cmds:
        raise ValueError('%s is already exposed!' % f.name)

    _cmds.append(f)

    def inner(*args, **kwargs):
        return f(*args, **kwargs)

    return inner

class Processor(object):
    """
    Lookup exposed_command method of implementation, return the result (a deferred).
    """

    preargs = []

    def __init__(self, implementation):
        self.processor_impl = implementation()
        for cmd in _cmds:
            setattr(self, 'exposed_%s' % cmd.__name__, cmd)

    def process(self, command, args = []):
        """
        Return a deferred that will be called back with the result of the command execution,
        if it is valid.

        Note that command-external preargs are passed to the execution proxy,
        to enable its use as an identifier.

        Any other exceptions are allowed to propagate here.
        """

        try:
            """
            Ensure args and preargs were set correctly, in particular that they
            are not simple strings.
            """
            self._checkArgType(args)
            self._checkArgType(self.preargs)
        except TypeError as e:
            d = defer.Deferred()
            d.errback(e)
            return d

        try:
            return getattr(self, 'exposed_%s' % command)(self.processor_impl, *(self.preargs + args))
        except AttributeError as e:
            d = defer.Deferred()
            d.errback(NoSuchCommand('%s was not found' % command))
            return d
        except TypeError as e:
            d = defer.Deferred()
            d.errback(WrongNumberOfArguments('%s does not expect %d args' % (command, len(args))))
            return d

    def _checkArgType(self, args):
        if hasattr(args, 'strip'):
            raise TypeError('args cannot be strings (use a list)')

        if not (hasattr(args, '__getitem__') or hasattr(args, '__iter__')):
            raise TypeError('args must be a list')
