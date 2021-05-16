import requests
import json
from headers import headers_crypto

def get_coins_details():
	url = "https://coinranking1.p.rapidapi.com/coins"
	response = requests.request("GET", url, headers=headers_crypto)

	resp_json = response.json()

	my_coins = ['eth', 'btc']#, 'xrp', 'ltc', 'bch', 'eos']

	list_of_my_coins = []

	for coin in resp_json['data']['coins']:
		if coin['symbol'].lower() in my_coins:
			temp_dict = {
				'coin_id': coin['id'],
				'coin_name': coin['name'],
			}
			list_of_my_coins.append(temp_dict)

	return list_of_my_coins

def main():
	my_coins = get_coins_details()
	with open('my_coins', 'w') as f:
		json.dump(my_coins, f)

if __name__ == '__main__':
	main()