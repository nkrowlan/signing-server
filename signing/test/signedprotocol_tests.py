from twisted.internet import defer
from twisted.test import proto_helpers
from twisted.trial import unittest

from signing.processor import Processor
from signing.signedprotocol import SignedProtocol, SignedProtocolFactory, InvalidSignature

class SignedProtocolTestCase(unittest.TestCase):
    """
    Trivial command implementation for test.
    """
    class DummyProcessor(object):
        def process(self, command, args):
            d = defer.Deferred()
            d.callback('result')
            return d
    """
    To avoid testing signing in this file, just append a letter as the signature.
    """
    class ClearSigner(object):
        def __init__(self, key):
            pass

        def signWithKey(self, key, data):
            return data + 'a'

        def sign(self, data):
            return data + 'a'

    """
    To avoid testing validation in this file, use a toggleable validation implementation.
    To remove signature, just remove the last letter.
    """
    class ToggleableValidation(object):
        valid = False
        signed_data = ''

        def validates(self, key, signed_data):
            return self.valid

        def removeSignature(self, key, signed_data):
            return signed_data[:-1]

    def setUp(self):
        self.processor = self.DummyProcessor()
        self.signer = self.ClearSigner('signing_key')
        self.validator = self.ToggleableValidation()

        factory = SignedProtocolFactory(self.processor, self.signer, self.validator)
        self.proto = factory.buildProtocol()
        self.tr = proto_helpers.StringTransportWithDisconnection()
        self.tr.protocol = self.proto
        self.proto.makeConnection(self.tr)

    def test_sign_failure_response(self):
        self.proto.clientkey = 'key1'
        self.validator.valid = False

        self.proto.lineReceived('this will fail to validate, according to validator')

        self.assertEquals(self.tr.value().strip(), self.signer.sign('invalid'))

    def test_sign_success_response(self):
        self.proto.clientkey = 'key1'
        self.validator.valid = True

        self.proto.lineReceived('this will validate, so we should not see result from processor')

        self.assertEquals(self.validator.removeSignature(None, (self.tr.value().strip())), 'result')

    def test_set_key(self):
        self.proto.clientkey = None
        key = 'key1'

        self.proto.lineReceived(key)

        self.assertEqual(self.proto.clientkey, 'key1')
