# Importing
from dotenv import load_dotenv
from requests import get
from datetime import date
import os
import datetime
import requests
import telegram_send

# Load from .env file
load_dotenv()
base_url = os.getenv('BASE_URL')
base_gecko = os.getenv('BASE_GECKO')
api_key = os.getenv('API_KEY') 
ether_value = 10 ** 18

# Function use to baking the URLs
def make_api_url(module, action, address, **kwargs):
	url = base_url + f"?module={module}&action={action}&address={address}&apikey={api_key}"

	for key, value in kwargs.items():
		url += f"&{key}={value}"

	return url

# Not used function to calculate the balance in ETH of a specific Ethereum address
def get_account_balance(address):
	balance_url = make_api_url("account", "balance", address, tag="latest")
	response = get(balance_url)
	data = response.json()

	value = int(data["result"]) / ether_value
	return f"ETH Balance: {value}"

# Function to query the Coingecko API to collect information regarding a specific token, based on it's contract 
def make_api_gecko_url(method, contractaddress, amount, recap):
    url = base_gecko + f"/{method}/ethereum/contract/{contractaddress}"
    telegram_send.send(messages=[recap])    # Send to Telegram the get_token_balance() output

    try:
        response = get(url, timeout=7)
        response.raise_for_status()
        data = response.json()
        image_url = data['image']['small']    # Not used token's thumb
        market_cap_rank = data['market_cap_rank']    # MCAP rank
        current_price = data['market_data']['current_price']['usd']     # Current price
        current_price = f"{current_price:8f}"   # Current token's price
        tx_value = float(amount) * float(current_price)     # The value of the tx
        tx_value = f"{tx_value:4f}"     # Format the tx value
        gecko_recap = f"MCAP Rank: {market_cap_rank}, \nCurr Price: ${current_price}, \nTx Value: ${tx_value}\n"
        telegram_send.send(messages=[gecko_recap])    # Send to Telegram the Coingecko's collected info
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

# Function to query the Etherscan.io API to get the balance for a specific Tx, based on token contract address and Ethereum Address 
def get_token_balance(address, contractaddress, tokenname, tokensymbol, time, tx_direction):
    token_balance_url = make_api_url("account", "tokenbalance", address, contractaddress=contractaddress, tag="latest")
    response = get(token_balance_url)
    data = response.json()
    token_amount = int(data['result'])    # Collect and calculate the token's amount from response
    token_amount = token_amount / ether_value
    if token_amount > 1:
        recap = f"Direction: {tx_direction}, \nTx Date: {time}, \nToken Name: {tokenname}, \nSymbol: {tokensymbol}, \nToken Amount: {token_amount:4f}"
        make_api_gecko_url(method='coins', contractaddress=contractaddress, amount=token_amount, recap=recap)

# Function to query the Etherscan.io API to get a list of ERC20 Tx(s) for a specific Ethereum address
def get_erc20_transactions(address):
    transactions_url = make_api_url("account", "tokentx", address, startblock=0, endblock=99999999, page=1, offset=10000, sort="desc")
    response = get(transactions_url)
    data = response.json()['result']    # Response to JSON
    pick_first = data[0]    # Pick the first result in response
    to = pick_first['to']    # The address in 'to'
    tokenname = pick_first["tokenName"]    # The token's name
    tokensymbol = pick_first["tokenSymbol"]    # The token's symbol
    contractaddress = pick_first["contractAddress"]    # The token's contract
    value = "{:,}".format(int(pick_first['value']))    # Tx value formatting
    time = datetime.datetime.utcfromtimestamp(int(pick_first['timeStamp']))    # Convert in UTC the EPOCH
    datetoday = date.today()    # Date of today
    is_today = time == datetoday    # Evaluation of the date of tx
    money_in = to.lower() == address.lower()    # Evaluation of to and from address
    if money_in:
        tx_direction = "IN"    # set to IN if to and from address are the same
    else:
        tx_direction = "OUT"    # set to OUT if to and from address are different
    if is_today:
        get_token_balance(address, contractaddress, tokenname=tokenname, tokensymbol=tokensymbol, time=time, tx_direction=tx_direction)
    else:
        telegram_send.send(messages=[f"Last Transaction: {tx_direction}, \nTx Date: {time}, \nToken Name: {tokenname}, \nSymbol: {tokensymbol}, \nValue: {value}"])