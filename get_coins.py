import requests
import json

def get_coins_details():
	url = "https://coingecko.p.rapidapi.com/coins/list"

	headers = {
    'x-rapidapi-host': "coingecko.p.rapidapi.com",
    'x-rapidapi-key': "3c33be481dmshfacd2991aed9fc9p1756adjsnd9543d717607"
    }

	response = requests.request("GET", url, headers=headers)

	resp_json = response.json()

	my_coins = ['eth', 'btc', 'xrp', 'ltc', 'bch', 'eos']

	list_of_my_coins = []
	for coin in resp_json:
		if coin['symbol'] in my_coins:
			list_of_my_coins.append(coin)

	return list_of_my_coins

def main():
	my_coins = get_coins_details()
	with open('my_coins', 'w') as f:
		json.dump(my_coins, f)

if __name__ == '__main__':
	main()