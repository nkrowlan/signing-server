from twisted.application import internet, service
from twisted.internet import reactor
from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile

from signing.commoncrypto import Validator, Signer
from signing.processor import Processor
from signing.processorimpl.sayhiimplementation import SayHiImplementation
from signing.signedprotocol import SignedProtocol, SignedProtocolFactory

port = 23456

processor = Processor(SayHiImplementation, ['say_hi'])
signer = Signer('dummyprivkey')
validator = Validator()

factory = SignedProtocolFactory(processor, signer, validator)

application = service.Application("Signed Execution Server")
internet.TCPServer(port, factory).setServiceParent(application)
logfile = DailyLogFile("signed_message_simple.log", ".")
#logfile = DailyLogFile("signed_message_simple.log", "/var/log/signing")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)
