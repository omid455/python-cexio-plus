import requests, hmac, hashlib, base64
from datetime import datetime

API_KEY = "51b24cfccbaf97b32a3d20dd0ea3863c265214a150e422d2dc910ec491ec4b27"
API_SECRET = "0d4dfa4dbc753d5046afcc666fc133c226701e9bebf04b50df33262ed0393f67"

# ACTION = "get_my_orders"
ACTION = "get_ticker"
PARAMS = '{"pair": "SOL-USD"}'

TIMESTAMP = int(datetime.now().timestamp())

PAYLOAD = ACTION + str(TIMESTAMP) + PARAMS

SIGNATURE = hmac.new(API_SECRET.encode(), PAYLOAD.encode(), hashlib.sha256).digest()
SIGNATURE = base64.b64encode(SIGNATURE)

res = requests.post(f"https://api.plus.cex.io/rest/{ACTION}",
              data=PARAMS,
              headers= {
                  'X-AGGR-KEY': API_KEY,
                  'X-AGGR-TIMESTAMP': str(TIMESTAMP),
                  'X-AGGR-SIGNATURE': SIGNATURE,
                  'Content-Type': 'application/json'
              })

if res.status_code != 200:
    print(f"request failed with status code {res.status_code}. Reason: {res.reason}")
    exit(-1)

# print(res.json())

coin_list = ["BTC-USD", "ETH-USD", "ETHW-USD", "ADA-USD", "SOL-USD", "MANA-USD", "AVAX-USD", "DOT-USD", "LINK-USD", "UNI-USD","XRP-USD"]  # , "DOGE-USD", "LUNC-USD"]
name_list = []
price_list = []
low_list = []
high_list = []
change_list = []

tickers = res.json()
# print(tickers)

number_of_coins = len(tickers["data"])


for coin in coin_list:
    index = 0
    # print(tickers["data"][coin_list[index]])
    while index < number_of_coins:
        if tickers["data"][coin_list[index]] == coin:
            coin_price = float(tickers["data"][index]["last"])
            low = float(tickers["data"][index]["low"])
            high = float(tickers["data"][index]["high"])
            percent = (low / high) * 100
            result_available = round(100 - percent, 2)
            name_list.append(tickers["data"][index]["pair"])
            price_list.append(coin_price)
            low_list.append(low)
            high_list.append(high)
            change_list.append(result_available)
        else:
            pass
        index = index + 1

index = 0
output = list()
output.append("Live Market Price:")

while index < 11:
    prices_list = name_list[index][:4], price_list[index], "Low:", low_list[index], "High:", high_list[index], "C:", \
        change_list[index]

    output.append(prices_list)
    index = index + 1