import requests
import json
from datetime import datetime
from headers import headers
from send_message import send_message as slack_message

def get_price(coin_id):
        url = "https://coinranking1.p.rapidapi.com/coin/{}".format(coin_id)

        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            price = response.json()['data']['coin']['price']
            return price
        else:
            print('Blad HTTP{}'.format(response.status_code))
            return '-1'

def main():
        currency = 'USD'
        with open('my_coins', 'r') as f:
                my_coins = json.load(f)

        prices = {}
        
        for coin in my_coins:
                price_precise = get_price(coin['coin_id'])
                price = round(float(price_precise), 2)
                prices[coin['coin_name']] = (price, currency)


        bit_price, bit_curr = prices['Bitcoin']
        eth_price, eth_curr = prices['Ethereum']

        #bitcoin_threshold = 8000
        #if prices['bitcoin'][0] < bitcoin_threshold:
        #       message = 'Bitcoin under {} -> {} {}'.format(bitcoin_threshold, bit_price, bit_curr)
        #       slack_message(message)

        #ethereum_threshold = 180
        #if prices['ethereum'][0] < ethereum_threshold:
        #       message = 'Ethereum under {} -> {} {}'.format(ethereum_threshold, eth_price, eth_curr)
        #       slack_message(message)
        
        message = 'Ethereum = {} {}\nBitcoin = {} {}'.format(eth_price, eth_curr, bit_price, bit_curr)
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
