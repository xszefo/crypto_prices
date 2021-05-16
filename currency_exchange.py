from headers import headers_exchange
import requests
import json

def get_currency_ratio(source, destination):
    url = 'https://currency-exchange.p.rapidapi.com/exchange'
    querystring = {
            "to": f"{destination}",
            "from": f"{source}",
            "q":"10"
    }

    print('Getting currency ratio...')

    response = requests.get(url, headers=headers_exchange, params=querystring)

    if response.status_code == 200:
        return float(response.json())
    
    raise Exception('Nie udalo sie pobrac danych')


def main():
    print(get_currency_ratio('USD', 'EUR'))


if __name__ == '__main__':
    main()