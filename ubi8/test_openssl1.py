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

    libcrypto = CDLL("libcrypto.so.1.1")
    assert libcrypto.FIPS_mode_set(1) != 0
    assert libcrypto.FIPS_mode() == 1

    unittest.main()
