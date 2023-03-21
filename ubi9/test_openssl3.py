import hashlib
import unittest


class TestFIPSModeAlgorithms(unittest.TestCase):
    def test_md5(self):
        with self.assertRaises(ValueError):
            hashlib.new("md5")

    def test_sha256(self):
        hashlib.new("sha256")


if __name__ == "__main__":
    from ctypes import CDLL

    libcrypto = CDLL("libcrypto.so.3")
    assert libcrypto.OSSL_PROVIDER_load(None, b"fips") != 0
    assert libcrypto.OSSL_PROVIDER_load(None, b"base") != 0
    assert libcrypto.EVP_set_default_properties(None, b"fips=yes") == 1

    unittest.main()
