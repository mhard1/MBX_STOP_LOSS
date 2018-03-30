import order
import requests
import sys
import urllib
import binance_socket

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

def get_available_balances(balance):

    raw_balance_list = balance.get('balances')
    
    place_holder_list = []

    available_balances = {}

    for i in range(len(raw_balance_list)):

        place_holder_list.append(i)

    for i in place_holder_list:

        if float(raw_balance_list[i].get('free')) > 0.00000000:
            
            asset_key = raw_balance_list[i].get('asset')
            asset_value = float(raw_balance_list[i].get('free'))
            
            available_balances[asset_key] = asset_value

    return available_balances

def check_if_order_is_possible(params, available_balances):
    
    parameters = params

    request_symbol = parameters.get('symbol')
    request_quantity = float(parameters.get('quantity'))
    
    request_order_side = parameters.get('side')

    balances = available_balances

    assets_list = list(balances.keys())

    asset_balance = 0.0
    
    for i in assets_list:

        if request_symbol.startswith(i):

            asset_balance = float(balances.get(i))
            asset_listing = i

    if request_order_side == 'SELL' and asset_balance >= request_quantity:
        
        return True
 
    else:
        print("Inadequate. Asset balance for %s is: %f" % (asset_listing, asset_balance))
        return False

def get_args(arguments):

    order_types = ['LIMIT', 'MARKET', 'TAKE_PROFIT', 'TAKE_PROFIT_LIMIT', 'STOP_LOSS', 'STOP_LOSS_MARKET','STOP_LOSS_LIMIT', 'LIMIT_MAKER']
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


def STOP_LOSS_MARKET(api_key, secret_key, params):

    trigger = params.get('price')
    
    params['type'] = 'MARKET'
    
    stop_loss_params = {i:params[i] for i in params if i!= 'price'}

    new_socket = binance_socket.Binsocket('bnbbtc', '@ticker', trigger) 

    status = (binance_socket.Binsocket.connected(new_socket))
    
    if status == True:

        user_order = order.Order(api_key, secret_key, stop_loss_params)        
        order.Order.test_Order(user_order)
        print("I WAS TRIGGERED!!!!")
    
    return 0

def main():
    
    api_key = input("\nPlease enter your API Key:" )
    secret_key = input("\nPlease enter your API Secret Key: ")
    
    user = order.Order(api_key, secret_key)
                
    balances_data = order.Order.check_Account(user)       
    
    available_balances = get_available_balances(balances_data)
    

    if len(sys.argv) > 1:
        
        arguments = sys.argv[1:]
    
        params = get_args(arguments)

    else:
        print("Parameter input error. Please check and try again.")
    
    
    order_possibility = check_if_order_is_possible(params, available_balances)

    if order_possibility == True:

        STOP_LOSS_MARKET(api_key, secret_key, params)

    else:
        print("You don't have a sufficient balance to perform this order")



if __name__ == "__main__":
    main() 




