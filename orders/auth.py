from django.core import signing
from datetime import datetime
import base64
import hashlib
import json
import random


LOGIN = '6dd490faf9cb87a9862245da41170ff2'
TRAN_KEY = '024h1IlD'


class RedirectionAuth:
    """ Generate Auth """
    def __init__(self, login=LOGIN, tran_key=TRAN_KEY):
        """ Constructor """
        self.login = login
        self.tran_key = tran_key
        self.nonce = str(random.random())
        self.seed = datetime.now().isoformat()

    # Base64(SHA - 1(nonce + seed + secretkey))
    def generate_tran_key(self):
        """ Generate trankey with nonce, seed and the tran_key """
        tran_k = str(self.nonce + self.seed + self.tran_key)
        return base64.b64encode(hashlib.sha1(tran_k.encode('utf-8')).digest())

    def get_nonce(self):
        """ Encode nonce """
        return base64.b64encode(self.nonce.encode('utf-8'))

    def get_auth(self):
        """ Get all the auth information """
        auth = {'login': self.login,
                'tranKey': self.generate_tran_key().decode('utf-8'),
                'nonce': self.get_nonce().decode('utf-8'),
                'seed': self.seed
                }
        return auth
