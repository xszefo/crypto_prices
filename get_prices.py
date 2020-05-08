import requests
import json
from datetime import datetime
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

	with open('prices', 'a') as f:
		f.write(str(datetime.now()))
		f.write('\n')
		for k,v in prices.items():
			result = '{id} = {price} {currency}\n'.format(id=k, price=v[0], currency=v[1])
			f.write(result)
		f.write(50*'*'+'\n')
		
if __name__ == '__main__':
	main()