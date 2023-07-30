'''
This is an HOTP implementation, it uses a counter to calculate each password.
'''

import otp
import hashlib

class HOTP(otp.OTP):
    def __init__(self, key:str, counter:int = 1, digits:int = 6, digest = hashlib.sha1):
        super().__init__(key, digits, digest)
        self.counter = counter
    
    def generate_next_otp(self, advance_counter = True):
        otp = super().generate_otp(self.counter)
        if advance_counter: self.counter += 1
        return otp