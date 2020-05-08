import requests
import json
from headers import headers

def get_price(coin_id, currency):
	url = "https://coingecko.p.rapidapi.com/simple/price"
	querystring = {
		"ids": {coin_id},
		"vs_currencies": {currency}
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	price = response.json()[coin_id][currency]

	return price

def main():
	currency = 'eur'
	with open('my_coins', 'r') as f:
		my_coins = json.load(f)

	prices = {}

	for coin in my_coins:
		price = get_price(coin['id'], currency)
		prices[coin['id']] = (price, currency)

	for k,v in prices.items():
		print('{id} = {price} {currency}'.format(id=k, price=v[0], currency=v[1]))
	
if __name__ == '__main__':
	main()