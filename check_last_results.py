from send_message import send_message as slack_message
from mysql.connector import connect, Error
from statistics import mean
import creds

def get_data_from_mysql(number_of_items):
    try:
        get_data_query = f'SELECT * FROM CURRENCY_VALUES ORDER BY id DESC LIMIT {number_of_items};'
        with connect(
                host='localhost', 
                user=creds.mysql['username'], 
                password=creds.mysql['password'],
                database='currencies',
                ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(get_data_query)
                    last_values = cursor.fetchall()
                    connection.commit()
                    cursor.close()
                connection.close()
        return last_values
    except Exception as err:
        print(err)

def main():
    """
    number_of_coins - liczba kryptowalut
    number_of_items - ile ostatnich wynikow danej kryptowaluty potrzebuje
    """
    number_of_coins = 3
    number_of_items = 3
    print(f'Checking last {number_of_items} results')
    last_values = get_data_from_mysql(number_of_items*number_of_coins)
    
    btc_values = [value[4] for value in last_values if value[3] == 1]
    eth_values = [value[4] for value in last_values if value[3] == 2] 
    doge_values = [value[4] for value in last_values if value[3] == 3]

    if (btc_mean:=mean(btc_values)) < 47000:
        slack_message(f'BTC: {btc_mean}')
    
    if (eth_mean:=mean(eth_values)) < 2900:
        slack_message(f'ETH: {eth_mean}')
    
    if (doge_mean:=mean(doge_values)) < 0.15:
        slack_message(f'DOGE: {doge_mean}')
    

if __name__ == '__main__':
    main()

        


