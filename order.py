import requests
import time
import hmac
import hashlib
import collections
import sys
import urllib


class Order:

    API_BASE = 'https://api.binance.com/api'
    
    HEADER = 'X-MBX-APIKEY'
    
    V1_VERSION = '/v1'
    V3_VERSION = '/v3'

    ORDER_TEST_PATH = '/order/test'

    RECV_WINDOW = '1000'

    TIME_STAMP = str(int(round(time.time() * 1000)))
    


    def __init__(self, key, secret, params):
        
        self.API_KEY = key
        self.API_SECRET = secret
        self.PARAMS = params
    
    def printargs(self):

        print("Your API Key is:" + self.API_KEY)

        print("Your Secret is:" + self.API_SECRET)
        print(self.PARAMS)


    def create_Header(self):

        header = {self.HEADER : self.API_KEY}

        return header

    def create_URL(self):

        version = self.V3_VERSION

        return self.API_BASE + version + self.ORDER_TEST_PATH


    def create_Signature(self):


        SECRET_ENCODED = self.API_SECRET.encode('utf-8')

        parameters = collections.OrderedDict()

        parameters.update(self.PARAMS)

        parameters['recvWindow'] = self.RECV_WINDOW
        parameters['timestamp'] = self.TIME_STAMP


        HASH_MESSAGE = urllib.parse.urlencode(parameters)

        HASH_MESSAGE_ENCODED = HASH_MESSAGE.encode('utf-8')

        h = hmac.new(SECRET_ENCODED, HASH_MESSAGE_ENCODED, hashlib.sha256)
        
        HASH_SIGNATURE = h.hexdigest()

        parameters['signature'] = HASH_SIGNATURE

        return parameters

    def test_Order(self):

        call = requests.post(Order.create_URL(self), headers=Order.create_Header(self), params=Order.create_Signature(self))

        print(call.json())

