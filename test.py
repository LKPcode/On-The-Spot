from get_data import BinanceAPI

client = BinanceAPI()



sell = [

    { 
        "asset": "BNB",
        "amount": 100
    }
]

buy = [
    {
        "asset":"SPARTA",
        "percent":50
    },
    {
        "asset":"STX",
        "percent":50
    }
]



# # res = client.execute_all_swaps_test(sell, buy)

# swap = {
#     "sell": "BTC",
#     "buy": "ETH",
#     "amount": 0.0001
# }
# res = client.find_route(swap)

# info = client.client.get_symbol_info('BNBBTC')

import json

file = open("keys.json")
dic = json.load(file)

file = open("keys.json", "w")
file.write(json.dumps(dic, indent=4))
file.close()