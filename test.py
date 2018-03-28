import order
import requests
import sys
import urllib


def get_symbols():    

    raw_data = requests.get('https://api.binance.com/api/v1/exchangeInfo')
    exchange_info = raw_data.json()
    raw_symbol_list = exchange_info.get('symbols')
    
    available_symbols = []

    for i in range(len(raw_symbol_list)):

        available_symbols.append(i)


    for i in available_symbols:

        available_symbols[i] = raw_symbol_list[i].get('symbol')
    
    return available_symbols



def get_args(arguments):

    order_types = ['LIMIT', 'MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_LIMIT', 'STOP_LOSS', 'STOP_LOSS_LIMIT', 'LIMIT_MAKER']
    order_side = ['BUY', 'SELL']
    timeInForce = ['FOK', 'IOC', 'GTC']
    symbols = get_symbols()
    price = 0.0
    
    params = {}

    
    for argument in arguments:
        
        if argument in symbols:
                
            params['symbol'] = argument


        elif argument in order_types:
                
            params['type'] = argument
        
        elif argument in order_side:
                
            params['side'] = argument
            
        elif argument in timeInForce:
                
            params['timeInForce'] = argument

        elif argument == '@':
            
            index = arguments.index('@')
            price_index = index + 1

            try:
                price = float(arguments[price_index]) 

                params['price'] = price
            
            except ValueError:
                pass
        else:
            
            if float(argument) != price:

                try:
                    float(argument)

                    quantity = argument
                
                    params['quantity'] = quantity
            
                except ValueError:
                    pass
            
            
    return params



def main():
    
    if len(sys.argv) > 1:
        arguments = sys.argv[1:]
    
    params = get_args(arguments)
    
    api_key = ''
    secret_key = ''

    user = order.Order(api_key, secret_key, params)

    order.Order.printargs(user)    
    
    order.Order.test_Order(user)

if __name__ == "__main__":
    main() 




