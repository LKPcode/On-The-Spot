from flask import Flask, request
from flask import jsonify
from get_data import *
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)

client = BinanceAPI()

@app.route("/api/spot-wallet-balances")
def balances():
        
    assets = client.get_spot_wallet_balances()
    assets =  client.assets_to_df(assets).to_dict("records")
    return jsonify(assets)


@app.route("/api/swap", methods = ['POST'])
def swap():
    data = request.json

    print(data)

    sell = [{"asset": asset["asset"] , "amount": asset["asset_amount"] } 
            for asset in data["sell"] ]
    buy = [{"asset": asset["asset"] , "percent": asset["asset_percentage"] } for asset in data["buy"] ]

    print("Executing TEST Swap")
    res = client.execute_all_swaps_test(sell, buy)
    if res["status"] == "ok":
        print("Executing REAL Swap")
        res = client.execute_all_swaps(sell, buy)
    print(res)
    return jsonify(res)


# app.run(host='127.192.0.0', port=5002)