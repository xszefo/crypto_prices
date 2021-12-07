import requests
import json
import creds
from mysql.connector import connect, Error
from datetime import datetime
from headers import headers_crypto
from send_message import send_message as slack_message
from currency_exchange import get_currency_ratio

def save_to_mysql(currency_code, crypto_code, value):
    print(f'Saving data to MYSQL database: 1 {crypto_code} = {value} {currency_code}')
    try:
        with connect(
                host='localhost', 
                user=creds.mysql['username'], 
                password=creds.mysql['password'],
                database='currencies',
                ) as connection:
            get_currency_query = f'SELECT * FROM CURRENCY_CODES where CODE="{currency_code}";'
            get_crypto_query = f'SELECT * FROM CRYPTO_CODES where CODE="{crypto_code}";'

            with connection.cursor() as cursor:
                cursor.execute(get_currency_query)
                currency_id = cursor.fetchall()[0][0]
            
                cursor.execute(get_crypto_query)
                crypto_id = cursor.fetchall()[0][0]

                insert_values_query = f'INSERT INTO CURRENCY_VALUES(currency_code_id, crypto_code_id, value) VALUES ({currency_id},{crypto_id},{value});'
                cursor.execute(insert_values_query)
                connection.commit()

    except Error as err:
        print('Saving to MYSQL database FAILED')
        print(err)
        return False

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
                ratio = 0.84 #To API przestalo dzialac -> get_currency_ratio(target_currency)

                price_in_euro = round(price*ratio, 10)
                prices[coin['coin_name']] = (coin['coin_symbol'], price_in_euro, currency)

                #print(f'COIN: {coin["coin_name"]}\nprice: {price} {currency}\nprice EUR: {price_in_euro}\nratio: {ratio} ')
        
        message = ''
        for coin, details in prices.items():
                '''
                Details to krotka ze szczegolami dla danej monety:
                details[0] - symbol kryptowaluty
                details[1] - wartosc kryptowaluty
                details[2] - waluta FIAT w ktorej podana jest wartosc
                '''
                message += f'{coin} = {details[1]} {target_currency}\n'
                save_to_mysql(target_currency, details[0], details[1])
        
        #print('Sending message to SLACK') 
        #slack_message(message)

        with open('prices', 'a') as f:
                f.write(str(datetime.now()))
                f.write('\n')
                for k,v in prices.items():
                        result = '{id} = {price} {currency}\n'.format(id=k, price=v[0], currency=v[1])
                        f.write(result)
                f.write(50*'*'+'\n')
        

if __name__ == '__main__':
        main()
        #currency_code = 'USD'
        #crypto_code = 'BTC'
        #value = '29423.06'

        #save_to_mysql(currency_code, crypto_code, value)
