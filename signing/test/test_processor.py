from twisted.internet import defer
from twisted.trial import unittest

from signing.processor import Processor, NoSuchCommand, WrongNumberOfArguments

class ProcessorTestCase(unittest.TestCase):
    class SayHiProcessorImplementation(object):
        """Trivial testing implementation."""
        def say_hi(self, identifier):
            d = defer.Deferred()
            d.callback('hello, %s' % identifier)
            return d

        def hidden_func(self):
            d = defer.Deferred()
            d.callback('this should never be exposed by the processor')
            return d

    def setUp(self):
        self.testcmd = 'say_hi'
        self.testdata = 'somedata'
        self.expected = 'hello, somedata'
        self.unexposed_command = 'hidden_func'
        self.processor = Processor(self.SayHiProcessorImplementation, [self.testcmd])

    def test_expected_processing_result_with_preargs(self):
        self.processor.preargs = [self.testdata]
        d = self.processor.process(self.testcmd)
        d.addCallback(self.assertEquals, self.expected)
        return d

    def test_expected_processing_result_no_preargs(self):
        self.processor.preargs = []
        d = self.processor.process(self.testcmd, [self.testdata])
        d.addCallback(self.assertEquals, self.expected)
        return d

    def test_valid_command_not_enough_args(self):
        self.processor.preargs = []
        d = self.processor.process(self.testcmd)
        return self.assertFailure(d, WrongNumberOfArguments)

    def test_no_such_command_no_preargs(self):
        self.processor.preargs = []
        d = self.processor.process('invalid_command')
        return self.assertFailure(d, NoSuchCommand)

    def test_no_such_command_with_args_no_preargs(self):
        self.processor.preargs = []
        d = self.processor.process('invalid_command', ['arg1', 'arg2'])
        return self.assertFailure(d, NoSuchCommand)

    def test_unexposed_function_no_preargs(self):
        self.processor.preargs = []
        d = self.processor.process(self.unexposed_command)
        return self.assertFailure(d, NoSuchCommand)

    def test_unexposed_function_with_preargs(self):
        self.processor.preargs = ['somearg']
        d = self.processor.process(self.unexposed_command)
        return self.assertFailure(d, NoSuchCommand)

    def test_invalid_preargs_set(self):
        self.processor.preargs = None
        d = self.processor.process(self.testcmd)
        return self.assertFailure(d, TypeError)

    def test_invalid_args_set(self):
        self.processor.preargs = [] 
        d = self.processor.process(self.testcmd, None)
        return self.assertFailure(d, TypeError)
