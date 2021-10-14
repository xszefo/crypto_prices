#!/bin/bash
uptime
cd '/home/piotr/Nauka/crypto_env'
source 'bin/activate'
cd '/home/piotr/Nauka/crypto_env/crypto_prices'
/usr/bin/python3.8 'get_prices.py'
/usr/bin/python3.8 'check_last_results.py'
echo '**************************'
