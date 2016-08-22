from twisted.trial import unittest

from signing.commoncrypto import Validator, Signer

class CommoncryptoTestCase(unittest.TestCase):
    """
    This is not intended to be a thorough test of the underlying cryptosystem,
    but just verifies that the functions essentially behave the way we might
    expect real ones to.
    """
    def setUp(self):
        self.validator = Validator()
        self.privkey = 'signing_key'
        self.signer = Signer(self.privkey)
        self.pubkey = self.signer.getPublicKey(self.privkey)

    def test_signed_data_validates(self):
        """Correctly signed data returns true"""
        data = 'somedata'
        self.assertTrue(self.validator.validates(self.pubkey, self.signer.sign(data)))

    def test_unsigned_data_fails(self):
        self.assertFalse(self.validator.validates('key1', 'someunsigneddata'))

    def test_sign_with_external_key_equivalent_to_internal(self):
        data = 'data'
        self.assertEqual(self.signer.sign(data), self.signer.signWithKey(self.signer.signing_key, data))

    def test_remove_signature(self):
        data = 'data'
        self.assertEqual(data, self.validator.removeSignature(self.pubkey, self.signer.sign(data)))
