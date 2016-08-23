signing-server
==============

A simple proof-of-concept demo using Twisted.

The premise of this project is to create a simple in-band-validated remote command execution server.

The signature scheme and command implementations are trivial at this point, just to provide enough
functionality to demonstrate the basic operation of the server.

There is no client implementation yet, but netcat functions well enough for now.

Operation
---------

A client connects and sends their public key, which is used by the server to validate all subsequent
messages:
```
$ nc helo.org 23456
mykey
```
The client then can send signed commands to the server, which it will validate, execute, and return
signed output in response. The only currently implemented command is `say_hi`, which responds with a
simple greeting:
```
say_himykey
hello, mykeyyekvirpymmud
```
Unimplemented commands, or commands with the wrong number of (space delimited) arguments will result in
an error message.

Running the server
------------------

This server should run on most systems with Twisted Python installed. The Twisted Application Framework
file [signing_server.tac](/signing_server.tac) provides a sample configuration and can be used to run the
server on port 23456.

Start the server with:
```
$ twistd -ny signing_server.tac
```
Log output can be monitored in `signed_message_simple.log`.

Extending functionality
-----------------------

To add additional commands, create an object with methods decorated by '''expose''' from [signing.processor](/signing/processor.py) that take the desired string arguments,
and instantiate the [Processor](/signing/processor.py) instance with the class name.
Instantiate the [SignedProtocolFactory](/signing/signedprotocol.py) with that processor,
and the decorated methods will be available to clients. See the included [SayHiImplementation](/signing/processorimpl/sayhiimplementation.py) and [signing_server.tac](/signing_server.tac).

Running tests
-------------

Unit tests in [signing/test/](/signing/test/) are written using Twisted's trial framework. Execute tests
using the `trial` tool provided with Twisted, for example:
```
$ trial signing
signing.test.test_commoncrypto
  CommoncryptoTestCase
    test_remove_signature ...                                              [OK]
    test_sign_with_external_key_equivalent_to_internal ...                 [OK]
    test_signed_data_validates ...                                         [OK]
[..]
```
