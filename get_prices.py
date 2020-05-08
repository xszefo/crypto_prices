import requests
import json

def get_prices(my_coins):
	for coin in my_coins:
		print(coin['id'])


def main():
	#with open('my_coins', 'r') as f:
	#	my_coins = json.load(f)

	with open('my_coins', 'r') as f:
		my_coins = json.load(f)

	print(my_coins)
	
if __name__ == '__main__':
	main()