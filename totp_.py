'''
This is an TOTP implementation, it uses the current time to calculate each password.
'''

import otp
from hashlib import sha1
from time import time
from math import floor
from typing import Optional


class TOTP(otp.OTP):
    def __init__(self, key, T0:int, X:int, digits:int = 6, digest = sha1):
        super().__init__(key, digits, digest)
        self.T0 = T0
        self.X = X
    
    def get_current_seed(self, epoch_:Optional[int] = None) -> int:
        if epoch_ is None:
            epoch_ = time()
        return floor((epoch_ - self.T0) / self.X)
    
    def generate_opt(self, from_epoch:Optional[int]=None, offset = 0):
        T = self.get_current_seed(from_epoch) + offset
        return super().generate_otp(T)
