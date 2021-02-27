import os
import requests
import json
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import httplib2
import time
import base64
import hmac

class Coinone:
    def __init__(self, version=1):
        self.server_url = 'https://api.coinone.co.kr/'
        self.api_url = f'{self.server_url}'
        self.market = {}


    def get_encoded_payload(self, payload):
        payload['nonce'] = int(time.time() * 1000)

        dumped_json = json.dumps(payload)
        encoded_json = base64.b64encode(bytes(dumped_json, 'utf-8'))
        return encoded_json


    def get_signature(self, encoded_payload):
        signature = hmac.new(SECRET_KEY, encoded_payload, hashlib.sha512)
        return signature.hexdigest()


    def get_response(self, action, payload, method='POST'):
        url = '{}{}'.format(self.api_url, action)

        encoded_payload = self.get_encoded_payload(payload)

        headers = {
            'Content-type': 'application/json',
            'X-COINONE-PAYLOAD': encoded_payload,
            'X-COINONE-SIGNATURE': self.get_signature(encoded_payload),
        }

        http = httplib2.Http()
        response, content = http.request(url, method, body=encoded_payload, headers=headers)

        return content
        
    def account_balance(self):        
        payload={'access_token': ACCESS_TOKEN }
        response = self.get_response(action='v2/account/balance', payload=payload)
        ret = json.loads(response)
        return ret



    def buy(self, symbol, price, qty, safety_check=True):
        if safety_check:
            current_price = self.price(symbol)
            if float(price) > float(current_price):
                print(f'You were trying to BUY {symbol} at price({price}) higher than the current price({current_price})!')
                return

        response = self.get_response(action='v2/order/limit_buy', payload={
            'access_token': ACCESS_TOKEN,
            'price': str(price),
            'qty': qty,
            'currency': symbol,
        })
        ret = json.loads(response)
        return ret


    def sell(self, symbol, price, qty, safety_check=True):
        if safety_check:
            current_price = self.price(symbol)
            if float(price) < float(current_price):
                print(f'You were trying to SELL {symbol} at price({price}) higher than the current price({current_price})!')
                return

        response = self.get_response(action='v2/order/limit_buy', payload={
            'access_token': ACCESS_TOKEN,
            'price': str(price),
            'qty': qty,
            'currency': symbol,
        })
        ret = json.loads(response)
        return ret


    def my_orders(self, symbol):
        response = self.get_response(action='v2/order/limit_orders', payload={
            'access_token': ACCESS_TOKEN,
            'currency': symbol,
        })
        ret = json.loads(response)
        return ret

    def cancel_order(self, symbol, order_id, price, qty, is_sell):
        response = self.get_response(action='v2/order/cancel', payload={
            'access_token': ACCESS_TOKEN,
            'order_id': order_id,
            'price': price,
            'qty': qty,
            'is_ask': is_sell,
            'currency': symbol,
        })
        ret = json.loads(response)
        return ret


    def cancel_last_order(self, symbol):
        orders = self.my_orders(symbol).get('limitOrders')
        if len(orders):
            order = orders[0]
            is_sell = 1 if order.get('type') == 'ask' else 0
            self.cancel_order(symbol, order.get('orderId'), order.get('price'), order.get('qty'), is_sell)


    def public_api(self, api, payload=None, method='GET'):
        url = f'{self.api_url}/{api}/'
        method = 'GET' if method.upper() not in ['GET', 'POST'] else method
        response = requests.request(method, url, params=payload)
        ret = json.loads(response.text)
        return ret
        
    def orderbook(self, symbol):
        payload={'currency':symbol}
        return self.public_api('orderbook', payload=payload)


    def price(self, symbol):
        payload={'currency':symbol}
        ret = self.public_api('ticker', payload=payload)
        return ret.get('last')

    
    def recent_trade(self, symbol):
        payload={'currency':symbol}
        ret = self.public_api('trades', payload=payload)
        return ret.get('completeOrders')



if __name__ == '__main__':
    ACCESS_TOKEN = access_token =os.environ['COINONE_ACCESS_TOKEN']
    SECRET_KEY = secret_key = bytes(os.environ['COINONE_SECRET_KEY'], 'utf-8')
    print(access_token)
    coinone = Coinone()

    #print(coinone.orderbook('ada'))
    print(coinone.price('ada'))
    print(coinone.recent_trade('ada'))
    balance = coinone.account_balance()
    print(balance.get('ada'))
    print(balance.get('btc'))
    print(balance.get('eth'))

    #print(coinone.buy('ada', 999, 11))
    print(coinone.my_orders('ada'))
    print(coinone.cancel_last_order('ada'))


