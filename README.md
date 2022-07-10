<h1 align="center">
  <br>
  Crypto Whales Tracking Telegram Bot (On Going Project)
  <br>
</h1>

<p align="center"><img src="whale.png" /></p>

<h4 align="center">A Telegram Bot to Tracking Ethereum and Bitcoin Whales</h4>



<p align="center">
  <a href="#key-features">Important Notes </a> •
  <a href="#key-features">How to configure </a> •
  <a href="#key-features">Key Features</a> •
  <a href="#credits">To do</a> •
   <a href="#credits">Credits</a> •
  <a href="#license">License</a>
</p>

## Important Notes

This Crypto Whales Alert Bot is design to send message to a Telegram Bot (yours) every time 
an Ethereum or Bitcoin whale will perform a IN or OUT Tx. The Idea is to track down the 
bigger Ethereum and Bitcoins whales to help you out to spot a new ERC20 token in case
of an Ethereum whale or to help you out to spot the potentially best moment to buy 
or sell your BTC


## How to configure

you need to create a .env file in your project folder with the following VARs

```bash
API_KEY=YOUR_Etherscan.io_Key
BASE_URL=https://api.etherscan.io/api
BASE_GECKO=https://api.coingecko.com/api/v3
```

to configure telegram_send pip package, if you need a virtual environment like me (folder venv), open a new Terminal 
in Visual Studio Code or Pycharm 


```
venv/bin/telegram-send configure

```

You will be asked to insert your token to access the HTTP API first, after that you have to insert the generated telegram-send
passwd to your bot, via client as message. In case of issues, you can also have a look at:

https://pypi.org/project/telegram-send/
https://www.rahielkasim.com/telegram-send/docs/api/


To find Ethereum whales, you can use Debank (https://debank.com/ranking), while to find Bitcoins whales have a look at:

https://www.youtube.com/watch?v=cxBQDWUNznc&list=WL&index=39 & https://www.youtube.com/watch?v=htq0i_ZdPY0&list=WL&index=40



## Key Features

* The List of Ethereum as well Bitcoin addresses can be customized
* Fully portable, this bot can runs on a VPS or whereever python 3.9.x is available


## To do

* Add Bitcoin Tracking Logic

## Credits

This code takes inspiration from:

https://github.com/techwithtim/Ethereum-Wallet-Tracker & https://github.com/nickpagz/btc-whale-tracker


## License

MIT

---

> GitHub [@cryptoshepherd](https://github.com/) &nbsp;&middot;&nbsp;
> Twitter [@the_lello](https://twitter.com/)

