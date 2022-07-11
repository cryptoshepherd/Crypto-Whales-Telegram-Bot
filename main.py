from datetime import timezone
import datetime
import time
import pandas
import telegram_send
import eth_functions

eth_addresses = {
    'PennilessWassie': "0x9c5083dd4838e120dbeac44c052179692aa5dac5",
    'YFImaxi': "0x50664ede715e131f584d3e7eaabd7818bb20a068"
}
btc_addresses = {
    'whale_1': "3QB2qhnj5Xxwhh3GKcfwQDSkL91BCCn5cp",
    'whale_2': "1Cr7EjvS8C7gfarREHCvFhd9gT3r46pfLb",
    'whale_3': "1BxgwUXszgVMrs9ZSfdcGLqne2vMYaW8jf",
    'whale_4': "3D8qAoMkZ8F1b42btt2Mn5TyN7sWfa434A",
    'whale_5': "39WQqCosC8ZD4S9XBPHRnnRUeVRvNctnnm",
    'whale_6': "1MDq7zyLw6oKichbFiDDZ3aaK59byc6CT8",
    'whale_7': "34MSicAL7qVGkevFPLwyc9KohGzoUSnu3Q",
    'whale_8': "3BMEXxSMT2b2kvsnC4Q35d2kKJZ4u9bSLh",
    'whale_9': "39gUvGynQ7Re3i15G3J2gp9DEB9LnLFPMN",
    'whale_10': "3EMVdMehEq5SFipQ5UfbsfMsH223sSz9A9",
    'whale_11': "1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ"
}

t_time = {}
amount = {}

for key in btc_addresses:
    t_time[key] = 0
    amount[key] = 0

check_again_eth = True
check_again_btc = True

while True:
    time.sleep(1)
    while check_again_eth:  # Starting the Ethereum whales check
        for whale in eth_addresses:
            address = eth_addresses[whale]
            eth_functions.get_erc20_transactions(address)
        check_again_eth = False

    while check_again_btc:
        for whale in btc_addresses:
            transactions_url = 'https://blockchain.info/rawaddr/' + btc_addresses[whale]
            df               = pandas.read_json(transactions_url)
            transactions     = df['txs']    # Pandas Dataframe
            last_time        = transactions[0]['time']    # Time of last tx       
            last_amount      = transactions[0]['result']    # Amount of last tx
            tx_time = datetime.datetime.utcfromtimestamp(last_time)    # Convert last tx time in UTC

            if last_time != t_time[whale]:
                t_time[whale] = last_time
                amount[whale] = last_amount

                if int(last_amount) > 0:    # Deterministic logic for Buy or Sell 
                    direction = "accumulating"
                elif int(last_amount) < 0:
                    direction = "dumping"

                btc_amount = int((float(abs(last_amount))/100000000))    # BTC amount calculation
                print(f'On {tx_time} {whale} is {direction} {btc_amount} BTC')
                telegram_send.send(messages=[f'On {tx_time}, {whale} is {direction} {btc_amount} BTC'])

            time.sleep(15)
        check_again_btc = False

    now = datetime.datetime.now(timezone.utc)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    minutes  = ((now - midnight).seconds) // 60

    if (minutes % 60) == 0:    # After an hour the counter is reset and the check go through one more time
        telegram_send.send(messages=['Whale watcher checking in.'])
        time.sleep(60)
        check_again_eth = True
        check_again_btc = True

