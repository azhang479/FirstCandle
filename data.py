import finnhub
from dotenv import load_dotenv
import os
import pandas as pd
import json
import websocket
import threading
from datetime import datetime
from zoneinfo import ZoneInfo

#dataset of candles
dataset = {}

load_dotenv()
api_key = os.getenv("API_KEY")
finnhub_client = finnhub.Client(api_key)

#prints out the message from the websocket
def on_message(ws, message):
    data = json.loads(message)        
    dump = (json.dumps(data, indent=2))
    if (data.get("type") == "trade"):
        print(dump)
        for trade in data.get("data"):
            #get relevant information
            t_ms = trade["t"]
            price = trade["p"]
            volume = trade["v"]
            ticker = trade["s"]
            t_min = t_ms // 60000
            
            #gets time info
            dt_et = datetime.fromtimestamp(t_ms / 1000, tz=ZoneInfo("America/New_York"))
            date = dt_et.date()
            hour = dt_et.hour
            minute = dt_et.minute

            print(f"{date}, {hour}, {minute}, {t_min}, {price}, {volume}, {ticker}")



#what to subscribe to when opening the websocket
def on_open(ws):
    tickers = ["BINANCE:BTCUSDT", "APPL"]
    for ticker in tickers:
        print(f"Connecting to {ticker}")
        ws.send(json.dumps({"type": "subscribe", "symbol": ticker}))


#when closing the websocket
def on_close(ws):
    print("### closed ###")


#script to stop websocket
def stop_ws():
    print("Stopping socket...")
    ws.close()


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        f"wss://ws.finnhub.io?token={api_key}",
        on_open=on_open,
        on_message=on_message,
    )

    timer = threading.Timer(20, stop_ws)
    timer.start()

    print("running")

    ws.run_forever()

