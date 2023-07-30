import unittest
import otp
import hotp
import pyotp


class Test_OTP(unittest.TestCase):
    def test_int_to_bytestring(self):
        a = otp.OTP.int_to_bytestring(1002)
        b = pyotp.OTP.int_to_bytestring(1002)
        self.assertEqual(a, b)

    def test_process_key(self):
        a = otp.OTP.process_key("HelloWorld")
        b = pyotp.OTP("HelloWorld").byte_secret()
        self.assertEqual(a, b)
    
    def test_generate_key(self):
        a = otp.OTP.generate_key()
        b = otp.OTP.generate_key()

        self.assertNotEqual(a, b)
    
    def test_OTP(self):
        a = otp.OTP("HelloWorld").generate_otp(1)
        b = pyotp.OTP("HelloWorld").generate_otp(1)
        self.assertEqual(a, b)


class Test_HOTP(unittest.TestCase):
    def test_generate_next_otp(self):
        a = hotp.HOTP("HelloWorld")
        b = otp.OTP("HelloWorld")

        self.assertEqual(a.generate_next_otp(), b.generate_otp(1))
        self.assertEqual(a.generate_next_otp(False), b.generate_otp(2))
        self.assertEqual(a.generate_next_otp(), b.generate_otp(2))
        self.assertEqual(a.generate_next_otp(), b.generate_otp(3))
        a.counter = 10
        self.assertEqual(a.generate_next_otp(), b.generate_otp(10))
        self.assertEqual(a.generate_next_otp(), b.generate_otp(11))


if __name__ == "__main__":
    unittest.main()