import requests
import json
from datetime import datetime
from headers import headers_crypto
from send_message import send_message as slack_message
from currency_exchange import get_currency_ratio

def get_price(coin_id):
        url = "https://coinranking1.p.rapidapi.com/coin/{}".format(coin_id)
        print('Getting crypto prices...')
        response = requests.request("GET", url, headers=headers_crypto)

        if response.status_code == 200:
            price = response.json()['data']['coin']['price']
            currency = response.json()['data']['base']['symbol']
            return float(price), currency
        else:
            print('Blad HTTP{}'.format(response.status_code))
            return '-1'

def main():
        with open('my_coins', 'r') as f:
                my_coins = json.load(f)

        prices = {}
        
        target_currency = 'EUR'

        for coin in my_coins:
                price, currency = get_price(coin['coin_id'])
                # Zamiana wartosci w walucie z API na EURO
                ratio = get_currency_ratio(target_currency)

                price_in_euro = round(price*ratio, 2)
                prices[coin['coin_name']] = (price_in_euro, currency)

                #print(f'COIN: {coin["coin_name"]}\nprice: {price} {currency}\nprice EUR: {price_in_euro}\nratio: {ratio} ')


        bit_price, bit_curr = prices['Bitcoin']
        eth_price, eth_curr = prices['Ethereum']
        doge_price, doge_curr = prices['Dogecoin']

        #bitcoin_threshold = 8000
        #if prices['bitcoin'][0] < bitcoin_threshold:
        #       message = 'Bitcoin under {} -> {} {}'.format(bitcoin_threshold, bit_price, bit_curr)
        #       slack_message(message)

        #ethereum_threshold = 180 
        #if prices['ethereum'][0] < ethereum_threshold:
        #       message = 'Ethereum under {} -> {} {}'.format(ethereum_threshold, eth_price, eth_curr)
        #       slack_message(message)
        
        message = ''
        for coin, details in prices.items():
                message += f'{coin} = {details[0]} {target_currency}\n'
        
        #message = f'Ethereum = {eth_price} {target_currency}\nBitcoin = {bit_price} {target_currency}'
        slack_message(message)

        with open('prices', 'a') as f:
                f.write(str(datetime.now()))
                f.write('\n')
                for k,v in prices.items():
                        result = '{id} = {price} {currency}\n'.format(id=k, price=v[0], currency=v[1])
                        f.write(result)
                f.write(50*'*'+'\n')
        

if __name__ == '__main__':
        main()
