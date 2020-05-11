import requests
import json
from datetime import datetime
from headers import headers
from send_message import send_message as slack_message

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


	bitcoin_threshold = 8000
	if prices['bitcoin'][0] < bitcoin_threshold:
		message = 'Bitcoin under {} {}'.format(bitcoin_threshold, prices['bitcoin'][1])
		slack_message(message)

	ethereum_threshold = 180
	if prices['ethereum'][0] < ethereum_threshold:
		message = 'Ethereum under {} {}'.format(ethereum_threshold, prices['ethereum'][1])
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
