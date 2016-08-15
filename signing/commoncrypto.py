# -*- test-case-name: signing.test.validator_tests -*-

"""
Validate that data is signed, strip signature from signed data, and sign data.

In this trivial implementation, signing is just appending the public key.
"""

from twisted.internet import defer

class Validator(object):
    """
    Signature validation operations.
    """

    def validates(self, key, signed_data):
        """
        Return whether signed_data was signed using a signer with the private key corresponding to
        the provided public key.
        """
        return signed_data.endswith(key)

    def removeSignature(self, key, signed_data):
        """
        Return the data part of the signed data.

        If the data isn't signed, the data is returned unmodified.
        """
        if self.validates(key, signed_data):
            idx = signed_data.rfind(key)
            return signed_data[:idx]
        else:
            return signed_data

class Signer(object):
    """
    Signing operations.
    """

    def __init__(self, signing_key):
        self.signing_key = signing_key
        self.public_key = self.getPublicKey(self.signing_key)

    def signWithKey(self, key, data):
        """
        Return data signed with private key.
        """
        return data + self.getPublicKey(key)

    def sign(self, data):
        """
        Return data signed with self.signing_key.
        """
        return self.signWithKey(self.signing_key, data)

    def getPublicKey(self, privkey):
        """
        Derive public key from the signing/private key.
        """
        return self.signing_key[::-1]
