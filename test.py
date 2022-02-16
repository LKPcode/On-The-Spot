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



# res = client.execute_all_swaps_test(sell, buy)

swap = {
    "sell": "BTC",
    "buy": "ETH",
    "amount": 0.0001
}
res = client.find_route(swap)