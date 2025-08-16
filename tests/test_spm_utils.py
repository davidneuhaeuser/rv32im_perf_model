import unittest

from perf_model.utility import btd_conversion


class TestUtils(unittest.TestCase):
    def test_btd_conversion(self):
        a: int = 0b1111 << 28
        b: int = 0b1100 << 28
        c: int = 0xFFFFFFFF
        d: int = 0b1000 << 28
        e: int = 0b0100 << 28
        # checked through binary converter
        self.assertEqual(btd_conversion(a), -268435456)
        self.assertEqual(btd_conversion(b), -1073741824)
        self.assertEqual(btd_conversion(c), -1)
        self.assertEqual(btd_conversion(d), -2147483648)
        self.assertEqual(btd_conversion(e), e)
