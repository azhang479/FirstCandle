import finnhub
from dotenv import load_dotenv
import os
import pandas as pd
import json
import websocket
import threading

load_dotenv()
api_key = os.getenv("API_KEY")

finnhub_client = finnhub.Client(api_key)

print("running")

#prints out the message from the websocket
def on_message(ws, message):
    data = json.loads(message)
    print(json.dumps(data, indent=2))

#what to subscribe to when opening the websocket
def on_open(ws):
    ws.send(json.dumps({"type": "subscribe", "symbol": "BINANCE:BTCUSDT"}))
    ws.send(json.dumps({"type": "subscribe", "symbol": "MSFT"}))

#when closing the websocket
def on_close(ws):
    print("### closed ###")

#script to stop websocket
def stop_ws():
    print("Stopping socket...")
    ws.close()

ws = websocket.WebSocketApp(
    f"wss://ws.finnhub.io?token={api_key}",
    on_open=on_open,
    on_message=on_message,
)

timer = threading.Timer(10, stop_ws)
timer.start()

ws.run_forever()