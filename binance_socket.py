import websocket
import ssl
from websocket import create_connection


class Websocket():

    BASE_ENDPOINT = "wss://stream.binance.com:9443/ws/"
    
    
    AGG_STREAM = "@aggTrade"
    
    TRADE_STREAM = "@trade"
    
    KLINE_STREAM = "@kline_"
    
    INDIVIDUAL_SYMBOL_TICKER = "@ticker"
    
    ALL_MARKET_TICKER = "!ticker@arr"
    
    PARTIAL_DEPTH = "@depth"
    
    DIFF_DEPTH = "@depth"

    KLINE_1m = "1m"
    KLINE_3m = "3m"
    KLINE_5m = "5m"
    KLINE_15m = "15m"
    KLINE_30m = "30m"
    
    KLINE_1h = "1h"
    KLINE_2h = "2h"
    KLINE_4h = "4h"
    KLINE_6h = "6h"
    KLINE_8h = "8h"
    KLINE_12h = "12h"
    
    KLINE_1d = "1d"
    KLINE_3d = "3d"
    
    KLINE_1w = "1w"

    KLINE_1M = "1M"

    DEPTH_LEVEL_5 = "5"
    DEPTH_LEVEL_10 = "10"
    DEPTH_LEVEL_20 = "20"

    
    def __init__(self, symbol, stream):
        self.SYMBOL = symbol
        self.STREAM = stream

    def websocket_connect(self):

        ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})

        ws.connect(self.BASE_ENDPOINT+self.SYMBOL+self.STREAM)
 
        run = True
        try:
            while run == True:
                print(ws.recv())
    
        except KeyboardInterrupt:
            run = False
    
        ws.close()

    
