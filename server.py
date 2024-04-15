from flask import Flask, request
from flask import jsonify
from get_data import *
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)

client = BinanceAPI()

@app.route("/api/spot-wallet-balances")
def balances():
    try: 
        assets = client.get_spot_wallet_balances()
        assets =  client.assets_to_df(assets).to_dict("records")
    except:
        pass
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


@app.route("/api/save-keys", methods = ['POST'])
def save_keys():
    res = client.saveNewKeys(request.json["api_key"], request.json["api_secret"])

    return jsonify({"message": res, "data": ""})


@app.route("/api/get-keys", methods = ['GET'])
def get_keys():
    res = client.getKeys()
    return jsonify(res)

if __name__ == "__main__":
    app.run() 
