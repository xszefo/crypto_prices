from headers import headers_exchange
import requests

def get_currency_ratio(destination):
    url = 'https://currencyscoop.p.rapidapi.com/latest'

    print('Getting currency ratio...')

    response = requests.get(url, headers=headers_exchange)

    if response.status_code == 200:
        # Zwrocona zostanie wartosc 1 USD w EURO
        return response.json()['response']['rates'][destination] 
    raise Exception('Nie udalo sie pobrac danych')


def main():
    print(get_currency_ratio('EUR'))


if __name__ == '__main__':
    main()