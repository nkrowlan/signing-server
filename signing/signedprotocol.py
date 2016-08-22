# -*- test-case-name: signing.test.test_signedprotocol -*-

from twisted.internet import protocol
from twisted.protocols.basic import LineReceiver
from twisted.python import log

from signing.processor import NoSuchCommand, WrongNumberOfArguments

class InvalidSignature(Exception):
    pass

class SignedProtocol(LineReceiver):
    """
    Simple line receiver that receives a public identifier upon connection.
    All subsequent lines of data are verified to be signed (based on the
    implementation of self.signer) before being split and passed to the
    processor. Any response is signed with signer, and returned to the
    client.
    """

    delimiter = '\n'

    def __init__(self, processor, signer, validator):
        self.processor = processor
        self.signer = signer
        self.validator = validator

    def lineReceived(self, line):
        log.msg('received line %s' % line)
        if self.clientkey is None:
            self.clientkey = line
            self.processor.preargs = [self.clientkey]
        elif self.validator.validates(self.clientkey, line):
            self.validDataReceived(self.validator.removeSignature(self.clientkey, line))
        else:
            log.msg('client %s failed validation of %s' % (self.clientkey, line))
            self.sendSignedLine('invalid')

    def validDataReceived(self, line):
        """
        Break the line up into command and arguments, and attempt to execute it.
        """
        log.msg('received valid data %s' % line)
        d = self.processor.process(*(lambda s: (s[0], s[1:]))(line.split()))
        d.addErrback(self.passClientErrors)
        d.addCallback(self.sendSignedLine)
        d.addErrback(log.err)
        return d

    def passClientErrors(self, failure):
        log.msg(failure.value)
        failure.trap(NoSuchCommand, WrongNumberOfArguments)
        return repr(failure.value)

    def sendSignedLine(self, data):
        if data != '':
            self.sendLine(self.signer.sign(data))

    def connectionMade(self):
        log.msg('received connection')
        self.clientkey = None

class SignedProtocolFactory(protocol.Factory):
    protocol = SignedProtocol

    def __init__(self, processor, signer, validator):
        self.params = (processor, signer, validator)

    def buildProtocol(self, *args):
        p = self.protocol(*self.params)
        p.factory = self
        return p
