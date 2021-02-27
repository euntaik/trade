import os
import requests
import json
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

class Upbeat:
    def __init__(self, version=1):
        self.server_url = 'https://api.upbit.com'
        self.api_url = f'{self.server_url}/v{version}'
        self.market = {}

    def markets(self):
        if not self.market:
            url = f'{self.api_url}/market/all'
            detail = 'true' if True else 'flase'
            querystring = {'isDetails':detail}
            response = requests.request('GET', url, params=querystring)
            results = json.loads(response.text)
            for entry in results:
                self.market[entry.get('market')] = entry
        
        return self.market

    def __symbol(self, symbol):
        symbol = f'KRW-{symbol.upper()}' if '-' not in symbol else symbol
        return symbol

    def price(self, ticksymboler, detail=False):
        url = f'{self.api_url}/ticker'
        symbol = self.__symbol(symbol)
        querystring = {'markets':{symbol}}
        response = requests.request('GET', url, params=querystring)
        data = response.json()[0]
        return data.get('trade_price') if not detail else data

    def candle_minutes(self, symbol, unit=1, to='', count=1):
        return self.candle(symbol, 'minutes', unit=unit, to=to, count=count)

    def candle(self, symbol, timespan, unit=1, to='', count=1):
        """
        parameters:
            symbol : 마켓 코드 (ex. KRW-BTC, BTC-BCC)
            duration : minutes, days, weeks, months
            unit : only valid for minute type. 분 단위. 가능한 값 : 1, 3, 5, 15, 10, 30, 60, 240
            to : 마지막 캔들 시각 (exclusive). 포맷 : yyyy-MM-dd'T'HH:mm:ssXXX or yyyy-MM-dd HH:mm:ss. 비워서 요청시 가장 최근 캔들
            count : 캔들 개수
        """
        symbol = self.__symbol(symbol)
        timespans = ['minutes', 'days', 'weeks', 'months']
        if timespan not in timespans:
            raise ValueError
        url = f'{self.api_url}/candles/{timespan}'
        url = f'{url}/{unit}' if timespan == 'minutes' else url
        print(url)
        querystring = {'market':symbol,'count':count}
        response = requests.request('GET', url, params=querystring)
        return response.json()

    def orderbook(self, symbol):
        symbol = self.__symbol(symbol)
        url = f'{self.api_url}/orderbook'
        querystring = {'markets':symbol}
        response = requests.request('GET', url, params=querystring)
        return response.json()

    def my_account(self, access_key, secret_key):
        url = f'{self.api_url}/accounts'
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }

        jwt_token = jwt.encode(payload, secret_key)
        authorize_token = 'Bearer {}'.format(jwt_token)
        headers = {'Authorization': authorize_token}

        res = requests.get(url, headers=headers)

        return res.json()

if __name__ == '__main__':
    access_key =os.environ['UPBIT_OPEN_API_ACCESS_KEY']
    secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
    upbeat = Upbeat()
    print(upbeat.my_account(access_key, secret_key))

    #ret = upbeat.markets()
    #print(ret)
    #ret = upbeat.price('ADA')
    #print(ret)
    #ret = upbeat.candle('ada', 'minutes')
    #print(ret)

    #print(upbeat.orderbook('ada'))
