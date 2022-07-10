import os
from dotenv import load_dotenv
from requests import get
from datetime import date, timezone
import datetime
import time
import requests
import telegram_send

load_dotenv()
base_url = os.getenv('BASE_URL')
base_gecko = os.getenv('BASE_GECKO')
api_key = os.getenv('API_KEY')
ether_value = 10 ** 18
eth_addresses = {
    'PennilessWassie': "0x9c5083dd4838e120dbeac44c052179692aa5dac5", 
    #'YFImaxi': "0x50664ede715e131f584d3e7eaabd7818bb20a068"
}

def make_api_url(module, action, address, **kwargs):
	url = base_url + f"?module={module}&action={action}&address={address}&apikey={api_key}"

	for key, value in kwargs.items():
		url += f"&{key}={value}"

	return url

def get_account_balance(address):
	balance_url = make_api_url("account", "balance", address, tag="latest")
	response = get(balance_url)
	data = response.json()

	value = int(data["result"]) / ether_value
	return f"ETH Balance: {value}"

def make_api_gecko_url(method, contractaddress, amount, recap):
    url = base_gecko + f"/{method}/ethereum/contract/{contractaddress}"
    telegram_send.send(messages=[recap])
    #telegram_send.send(messages=["Token Balance"])
    try:
        response = get(url, timeout=7)
        response.raise_for_status()
        data = response.json()
        image_url = data['image']['small']
        market_cap_rank = data['market_cap_rank']
        current_price = data['market_data']['current_price']['usd']
        current_price = f"{current_price:8f}"
        tx_value = float(amount) * float(current_price)
        tx_value = f"{tx_value:4f}"
        gecko_recap = f"Market CAP Rank: {market_cap_rank}, \nCurrent Price: ${current_price}, \nTx Value: ${tx_value}\n"
        telegram_send.send(messages=[gecko_recap])
        #telegram_send.send(messages=["Gecko Recap"])
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

def get_token_balance(address, contractaddress, tokenname, tokensymbol, time, tx_direction):
    token_balance_url = make_api_url("account", "tokenbalance", address, contractaddress=contractaddress, tag="latest")
    response = get(token_balance_url)
    data = response.json()
    token_amount = int(data['result'])
    token_amount = token_amount / ether_value
    if token_amount > 1:
        recap = f"Direction: {tx_direction}, \nTx Date: {time}, \nToken Name: {tokenname}, \nToken Symbol: {tokensymbol}, \nToken Amount: {token_amount:4f}"
        make_api_gecko_url(method='coins', contractaddress=contractaddress, amount=token_amount, recap=recap)

def get_erc20_transactions(address):
    transactions_url = make_api_url("account", "tokentx", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="asc")
    response = get(transactions_url)
    data = response.json()['result']
    # Sort Transaction per TimeStamp
    data.sort(key=lambda x: int(x['timeStamp']))
    
    for tx in data:
        to = tx["to"]
        tokenname = tx["tokenName"]
        tokensymbol = tx["tokenSymbol"]
        contractaddress = tx["contractAddress"]
        if "gasPrice" in tx:
            gas = int(tx["gasUsed"]) * int(tx["gasPrice"]) / ether_value
        else:
            gas = int(tx["gasUsed"]) / ether_value
        time = datetime.datetime.fromtimestamp(int(tx['timeStamp']))
        datetoday = date.today()
        is_today = time == datetoday
        money_in = to.lower() == address.lower()
        if money_in and is_today:
            tx_direction = "IN"
            get_token_balance(address, contractaddress, tokenname=tokenname, tokensymbol=tokensymbol, time=time, tx_direction=tx_direction)
        if not money_in and is_today:
            tx_direction = "OUT"
            get_token_balance(address, contractaddress, tokenname=tokenname, tokensymbol=tokensymbol, time=time, tx_direction=tx_direction)

check_again = True

while True:
    time.sleep(1)
    while check_again:
        for whale in eth_addresses:
            address = eth_addresses[whale]
            get_erc20_transactions(address)
        check_again = False

    now = datetime.datetime.now(timezone.utc)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    minutes  = ((now - midnight).seconds) // 60

    if (minutes % 60) == 0:
        telegram_send.send(messages=['Whale watcher checking in.'])    
        time.sleep(60)
        check_again = True