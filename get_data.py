from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException
import pandas as pd
import json


class BinanceAPI:

    def __init__(self):
        #Real Binance
        self.api_key = ""
        self.api_secret = ""
        self.setKeys()
        self.testnet = False
        
        #Testent Binance
        # api_key = "DazYFin7onDM9jLQIYlo372ntGjF81aOkn7l8Pe9m0OcRzTTnOIdeRnyMCOq4E8O"
        # api_secret = "8eLuStULGTwIeAIg2u4mlpkoB4sBbEPvOso9dkSNe017ZHqQopBEn8jtTSQ1lIbz"
        self.client = Client(self.api_key, self.api_secret, testnet=self.testnet)

    def saveNewKeys(self, api_key, api_secret):
        content = {
                    "keys": {
                        "api_key": api_key,
                        "api_secret": api_secret 
                    }
                }
        print("Save Keys: ",content)
        file = open("keys.json", "w")
        file.write(json.dumps(content, indent=4))  
        file.close()
        self.setKeys()
        self.client = Client(self.api_key, self.api_secret, testnet=self.testnet)
        return "Keys Saved" 

    def setKeys(self):
        file = open("keys.json")
        content = json.load(file)
        file.close()
        self.api_key = content["keys"]["api_key"] 
        self.api_secret = content["keys"]["api_secret"]

        print("Keys Set: ",self.api_key,  self.api_secret )

    def getKeys(self):
        file = open("keys.json") 
        return json.load(file)


    def get_spot_wallet_balances(self):
        balances = self.client.get_account()["balances"]
        assets = [x for x in balances if float(x["free"]) > 0 or float(x["locked"]) > 0]
        prices = self.client.get_all_tickers()

        for i in range(len(assets)):
            pair = assets[i]["asset"] + "BTC"

            price = list(filter(lambda symbol: symbol['symbol'] == pair , prices))
            assets[i]["total"] = float(assets[i]["free"]) + float(assets[i]["locked"]) 

            if assets[i]["asset"] == "BTC": #BTC
                assets[i]["price"] = assets[i]["total"]
            elif len(price) > 0: #Cryptocurrency with BTC as quote asset
                assets[i]["price"] = float(assets[i]["total"]) * float(price[0]["price"])
            else: # Stabelecoin
                symbol = [x for x in prices if x["symbol"] == "BTC" + assets[i]["asset"]]
                if len(symbol) > 0:
                    assets[i]["price"] = float(assets[i]["total"]) / float(symbol[0]["price"])
                else: # Coin with no pairs ?
                    assets[i]["price"] = 0.0

        btc_price = float(self.client.get_avg_price(symbol='BTCBUSD')["price"])
        for i in range(len(assets)):
            assets[i]["usd_value"] = float(assets[i]["price"]) * btc_price

        return assets

    def assets_to_df(self,assets):
        
        assets_pd = pd.DataFrame(assets)
        assets_pd = assets_pd.sort_values(by="usd_value", ascending=False)
        df = assets_pd
        df["coin_price"] = df["usd_value"] / df["total"]
        df["percentage"] = df["usd_value"] / df["usd_value"].sum() * 100
        df = df[df["percentage"] > 0.1]
        return df

    def total_balance(self,assets):
        # Total value of portofolio
        return "{:0.0{}f}".format(float(sum(asset["usd_value"] for asset in assets)), 2)


    def round_step_size(self,quantity, step_size):
        import math
        """Rounds a given quantity to a specific step size
        :param quantity: required
        :param step_size: required
        :return: decimal
        """
        precision: int = int(round(-math.log(step_size, 10), 0))
        return float(round(quantity, precision))


    def create_market_order_by_quote(self,symbol, side, quoteOrderQty, test=False):
        symbol_info = self.client.get_symbol_info(symbol)
        filters = symbol_info["filters"]
        
        #### FILTERS ####
        #MIN_NOTIONAL filter
        filter_ = [x for x in filters if x["filterType"] == "MIN_NOTIONAL" ][0]
        if quoteOrderQty < float(filter_["minNotional"]):
            res = {"message": f"Quote Order Quantity must be higher than {filter_['minNotional']}",
                    "type" : "MIN_NOTIONAL"}
            print(res)
            return res

        qty = "{:0.0{}f}".format(quoteOrderQty, symbol_info["quoteAssetPrecision"])

        try:
            if test == False:
                order = self.client.create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quoteOrderQty= qty,
                )
            else: 
                order = self.client.create_test_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quoteOrderQty= qty,
                )

        except BinanceAPIException as s:
            res = {"message" : str(s) , "type": "BinanceAPIException"}
            print(res)
            return res 

        return order

    #res = create_market_order_by_quote('BTCUSDT',SIDE_BUY ,0.0000010)



    def create_market_order(self,symbol, side, quantity, test=False):
        symbol_info = self.client.get_symbol_info(symbol)
        avg_price = float(self.client.get_avg_price(symbol= symbol)["price"])
        filters = symbol_info["filters"]
        
        #### FILTERS ####
        #MARKET_LOT_SIZE filter
        filter_ = [x for x in filters if x["filterType"] == "MARKET_LOT_SIZE" ][0]
        if not ((float(filter_["maxQty"]) > quantity > float(filter_["minQty"]))):
            res = {"message": f"Quantity must be in the range ({filter_['minQty'] } - { filter_['maxQty']}]",
                    "type" : "MARKET_LOT_SIZE"}
            print(res)
            return res
        #MIN_NOTIONAL filter
        filter_ = [x for x in filters if x["filterType"] == "MIN_NOTIONAL" ][0]
        if quantity * avg_price < float(filter_["minNotional"]):
            res = {"message": f"Quote Order Quantity must be higher than {filter_['minNotional']}, Base asset Quantity must be higher than { float(filter_['minNotional']) / avg_price} {symbol_info['baseAsset']}",
                    "type" : "MIN_NOTIONAL"}
            print(res)
            return res
        #LOT_SIZE filter
        filter_ = [x for x in filters if x["filterType"] == "LOT_SIZE" ][0]
        quantity = self.round_step_size(quantity, float(filter_["stepSize"]))
        if not ( float(filter_["maxQty"]) > quantity > float(filter_["minQty"])):
            res = {"message": f"Quote Order Quantity must be higher than {filter_['minQty']}, Base asset Quantity must be higher than { float(filter_['minQty']) / avg_price} {symbol_info['quoteAsset']}",
                    "type" : "LOT_SIZE"}
            print(res)
            return res
        
        try:
            qty = "{:0.0{}f}".format(quantity, symbol_info["baseAssetPrecision"])
            print(f"{side} order for {qty} {symbol}")
            if test == False:
                order = self.client.create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity= qty,
                )
            else:
                order = self.client.create_test_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity= qty,
                )

        except BinanceAPIException as s:
           res = {"message" : str(s) , "type": "BinanceAPIException"}
           print(res)
           return res 
            
        return order

    # res = create_market_order('STXUSDT',SIDE_BUY ,11)
    # res

    ### FINDING ROUTE ###

    #

    def find_route(self,swap):
        prices = self.client.get_all_tickers()
        tickers = [x["symbol"] for x in prices]


        if not any(swap["sell"] in symbol for symbol in tickers):
            print(swap["sell"], " does not exist")
            return []
        if not any(swap["buy"] in symbol for symbol in tickers):
            print(swap["buy"], " does not exist")
            return []

        path = []


        direct_swap = [x for x in tickers if x == swap["sell"] + swap["buy"] or x == swap["buy"] + swap["sell"]]

        if direct_swap:
            path.append(direct_swap[0])
            return path
        else:
            second_symbol_list = ["BNB","BTC","USDT","BUSD"]
            for symbol in second_symbol_list:
                base_swap = [symbol for x in tickers if x == swap["sell"] + symbol or x == symbol + swap["sell"]]
                quote_swap = [symbol for x in tickers if x == swap["buy"] + symbol or x == symbol + swap["buy"]]
                if base_swap and quote_swap:
                    path.append([x for x in tickers if x == swap["sell"] + symbol or x == symbol + swap["sell"]][0])
                    path.append([x for x in tickers if x == swap["buy"] + symbol or x == symbol + swap["buy"]][0])
                    return path

        for symbol in second_symbol_list:
            base_swap = [symbol for x in tickers if x == swap["sell"] + symbol or x == symbol + swap["sell"]]
            if base_swap:
            
                path.append([x for x in tickers if x == swap["sell"] + symbol or x == symbol + swap["sell"]][0])
                break

        for symbol in second_symbol_list: 
                quote_swap = [symbol for x in tickers if x == swap["buy"] + symbol or x == symbol + swap["buy"]]
                if quote_swap:  
                    path.append("")
                    path.append([x for x in tickers if x == swap["buy"] + symbol or x == symbol + swap["buy"]][0])
                    break

        for symbol in second_symbol_list:
            next_swap  = [x for x in tickers if x == base_swap[0] + quote_swap[0] or x == quote_swap[0] + base_swap[0] ]
            if next_swap:
                path[1] = next_swap[0]
    


    ### TAKING SIDES ###
    def get_sides_path(self,asset_to_sell, path):
        def find_side(symbol, pair):
            position = pair.find(symbol)
            if position == -1:
                print("There was an error in 'get_sides_path'")
            if position == 0:
                return "SELL"
            else: 
                return "BUY"

        sides_path = []
        ticker_1 = asset_to_sell
        for pair in path:
            sides_path.append(find_side(ticker_1, pair))
            ticker_1 = pair.replace(ticker_1 , "")
        print("SIDES: ", sides_path)
        return sides_path

    # sides_path = get_sides_path(swap["sell"], path)


    def execute_market_orders(self,path, sides_path, quantity, test=False):
        response = []
        for i in range(len(path)):
            print(f"Executing {path[i]}")
            if sides_path[i] == "SELL":
                res = self.create_market_order(path[i], sides_path[i] , quantity, test)
            else:
                res = self.create_market_order_by_quote(path[i], sides_path[i] , quantity, test)
            if "cummulativeQuoteQty" in res:         
                quantity = float(res["cummulativeQuoteQty"])
            else: return res
            response.append(res)
        return response


    def execute_swap(self,swap, test=False):
        path = self.find_route(swap)
        sides_path = self.get_sides_path(swap["sell"], path)
        return self.execute_market_orders(path, sides_path, swap["amount"], test)
        
        
    def price_convertion(self,base,quote, amount):
        tickers = self.client.get_all_tickers()
        path = self.find_route({"sell":base,"buy":quote})
        print(path)
        sides_path = self.get_sides_path(base, path)

        asset_price = amount
        for i in range(len(path)):
            price = float(list(filter(lambda pair: pair['symbol'] == path[i], tickers))[0]["price"])
            if sides_path[i] == "SELL":
                asset_price = asset_price * price
            else: asset_price = price / asset_price

        return asset_price


        
    def execute_all_swaps(self,sell, buy, aggrigation_coin="BTC"):
        #create swap Dicts
        sell_swaps = []
        target_coin = aggrigation_coin
        target_coin_amount = 0
        for asset in sell:
            if asset["asset"] == target_coin:
                target_coin_amount = asset["amount"]
            else:   
                sell_swaps.append({
                    "sell": asset["asset"],
                    "buy": target_coin,
                    "amount": asset["amount"]
                })

        sell_responses = []
        for swap in sell_swaps:
            sell_responses.append(self.execute_swap(swap))

        print(sell_responses)

        if all([ isinstance(res, list) for res in sell_responses]):
            value_sold = sum(float(res[-1]["cummulativeQuoteQty"]) for res in sell_responses) + target_coin_amount
            print(self.price_convertion(target_coin,"BUSD",  value_sold))
        else: return {"status": "error", "message": "An error occured while executing sell orders",  "errors": sell_responses }
        buy_swaps = []
        for asset in buy:
            buy_swaps.append({"sell":target_coin, "buy":asset["asset"] , "amount":  value_sold * asset["percent"] / 100  })

        buy_responses = []
        for swap in buy_swaps:
            buy_responses.append(self.execute_swap(swap))
        print(buy_responses)

        if all([ isinstance(res, list) for res in buy_responses]):
            value_sold = sum(float(res[-1]["cummulativeQuoteQty"]) for res in buy_responses) + target_coin_amount
            print(self.price_convertion(target_coin,"BUSD",  value_sold))
        else: return {"status": "error", "message": "An error occured while executing buy orders", "errors": buy_responses }


        return {"sell_responses": sell_responses, "buy_responses":buy_responses, "status": "ok", "message": "Swap was successful"}



    def execute_all_swaps_test(self,sell, buy, aggrigation_coin="BTC"):

        problem_occured = False
        #create swap Dicts
        sell_swaps = []
        target_coin = aggrigation_coin
        for asset in sell:
            sell_swaps.append({"sell": asset["asset"], "buy": target_coin, "amount": asset["amount"]})

        sell_responses = []
        for swap in sell_swaps:
            sell_responses.append(self.execute_swap(swap, test=True))

        print(sell_responses)

        if not all(x=={} for x in sell_responses):
            problem_occured = True


        value_sold = sum([ self.price_convertion(x["asset"], target_coin, x["amount"]) for x in sell])
        print(self.price_convertion(target_coin,"BUSD",  value_sold))

        buy_swaps = []
        for asset in buy:
            buy_swaps.append({"sell":target_coin, "buy":asset["asset"] , "amount":  value_sold * asset["percent"] / 100  })

        buy_responses = []
        for swap in buy_swaps:
            buy_responses.append(self.execute_swap(swap, test=True))

        print(buy_responses)

        status = "error" if problem_occured == True else "ok"

        return {"sell_responses": sell_responses, "buy_responses":buy_responses, "status": status }

