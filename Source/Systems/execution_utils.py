
import requests
import json
import hmac
import hashlib
import time
from datetime import datetime



def latest_filter(apiKey, secretKey, client_order_id=None, settle_type=None):
    timestamp = '{0}000'.format(int(time.mktime(datetime.now().timetuple())))
    method    = 'GET'
    endPoint  = 'https://forex-api.coin.z.com/private'
    path      = '/v1/latestExecutions'

    text = timestamp + method + path
    sign = hmac.new(
        secretKey.encode('ascii'),
        text.encode('ascii'),
        hashlib.sha256
    ).hexdigest()

    parameters = {
        "symbol": "USD_JPY",
        "count": 100
    }

    headers = {
        "API-KEY": apiKey,
        "API-TIMESTAMP": timestamp,
        "API-SIGN": sign
    }

    res = requests.get(endPoint + path, headers=headers, params=parameters)
    data = res.json()

    results = data["data"]["list"]

    # 🔍 フィルタ処理
    filtered = []
    for item in results:
        # clientOrderIdで絞る
        if client_order_id and item["clientOrderId"] != client_order_id:
            continue

        # settleTypeで絞る
        if settle_type == "CLOSE" and item["settleType"] != "CLOSE":
            continue
        elif settle_type == "OPEN" and item["settleType"] != "OPEN":
            continue
        elif settle_type == "ALL":
            pass  # 両方OK

        filtered.append(item)

    return filtered

def extract_field(data_list, field_name):
    return [
        item[field_name]
        for item in data_list
        if field_name in item
    ]


# filtered = latest_filter(apiKey, secretKey, settle_type="ALL")

# fees = extract_field(filtered, "fee")
