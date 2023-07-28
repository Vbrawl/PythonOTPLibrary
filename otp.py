'''
This file was created with the help of RFC4226, section 5.3.
It contains all nescessary functions for generating HOTP codes.

All variables have similar names to the one's in the document and
some may have exactly the same name.
'''

import base64
import hmac
import hashlib
import time, os, random, psutil
psutil.cpu_percent() # Ensure that this function will return something next time

LAST_KEY_SEED = None

class OTP:
    def __init__(self, key:str, digits:int = 6, digest = hashlib.sha1):
        self.key = OTP.process_key(key)
        self.digits = digits
        self.digest = digest
    
    def generate_otp(self, Counter:int):
        # Snum = HS.digest()
        Snum = hmac.new(self.key, OTP.int_to_bytestring(Counter), self.digest).digest()
        offset = Snum[-1] & 0xF
        Snum = (
            Snum[offset] << 24
            | Snum[offset + 1] << 16
            | Snum[offset + 2] << 8
            | Snum[offset + 3]
        ) & 0x7FFFFFFF
        return str(Snum % 10**self.digits).rjust(self.digits, '0')
    
    @staticmethod
    def process_key(key:str) -> bytes:
        pad = len(key) % 8
        key += '=' * (8 - pad)
        return base64.b32decode(key, casefold=True)
    
    @staticmethod
    def int_to_bytestring(value:int) -> bytes:
        result = bytearray()
        while value != 0:
            result.append(value & 0xFF)
            value >>= 8
        
        return bytes(reversed(result)).rjust(8, b'\0')
    
    @staticmethod
    def generate_key():
        global LAST_KEY_SEED

        FinalSeed = b''
        # Get OS live time
        # FinalSeed += OTP.int_to_bytestring(5)
        FinalSeed += OTP.int_to_bytestring(int(time.time() - psutil.boot_time()))
        # Get CPU load
        # FinalSeed += OTP.int_to_bytestring(5)
        FinalSeed += OTP.int_to_bytestring(int(psutil.cpu_percent()))
        # Get RAM usage
        FinalSeed += OTP.int_to_bytestring(psutil.virtual_memory().used)
        # Get EPOCH
        FinalSeed += OTP.int_to_bytestring(int(time.time()))
        # Get A random number from os.urandom
        FinalSeed += os.urandom(32)

        if LAST_KEY_SEED is not None:
            half_length = len(FinalSeed) // 2
            LAST_KEY_SEED_LENGTH = len(LAST_KEY_SEED)
            FinalSeed += bytes(random.choices(LAST_KEY_SEED, k = LAST_KEY_SEED_LENGTH - half_length))
        LAST_KEY_SEED = FinalSeed

        return hashlib.sha3_512(FinalSeed)