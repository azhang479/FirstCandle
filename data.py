import finnhub
from dotenv import load_dotenv
import os
import pandas as pd
import json
import websocket
import threading
from datetime import datetime
from zoneinfo import ZoneInfo
from candle import Candle

#dataset of candles
dataset = {}
tick = True

load_dotenv()
api_key = os.getenv("API_KEY")
finnhub_client = finnhub.Client(api_key)

#prints out the message from the websocket
def on_message(ws, message):
    global dataset
    data = json.loads(message)        
    dump = (json.dumps(data, indent=2))
    if (data.get("type") == "trade"):
        for trade in data.get("data", []):
            #get relevant information
            t_ms = trade.get("t", -1)
            price = trade.get("p", -1)
            volume = trade.get("v", -1)
            ticker = trade.get("s", -1)

            if (t_ms == -1 or price == -1 or volume == -1 or ticker == -1):
                print("Error values, trade skipped.")
                continue

            #gets time info
            dt_et = datetime.fromtimestamp(t_ms / 1000, tz=ZoneInfo("America/New_York"))
            date = dt_et.date()
            hour = dt_et.hour
            minute = dt_et.minute
            index = f"{hour:02d}:{minute:02d}"

            tickerDict = dataset.get(ticker)

            if (index in dataset.get(ticker)):
                cand = tickerDict.get(index)
                cand.updateCandle(price, volume)
            else:
                tickerDict[index] = Candle(minute, price, volume)


#what to subscribe to when opening the websocket
def on_open(ws):
    global dataset
    global tick
    tickers = ["BINANCE:BTCUSDT", "BINANCE:ETHUSDT"]
    for ticker in tickers:
        print(f"Connecting to {ticker}")
        ws.send(json.dumps({"type": "subscribe", "symbol": ticker}))
        dataset.update({ticker:{}})


#when closing the websocket
def on_close(ws):
    print("### closed ###")
    print(dataset)


#script to stop websocket
def stop_ws():
    global dataset
    global tick
    print("Stopping socket...")

    #mark first and last as unusable since not full candles
    for ticker in dataset:
        tickerDict = dataset.get(ticker)
        tickerDict.get(list(tickerDict)[0]).setUnusable()
        tickerDict.get(list(tickerDict)[-1]).setUnusable()

    tick = False
    print(dataset)
    ws.close()


def second_count(count):
    if (tick):
        print(count)
        seconds = threading.Timer(1, second_count, args=(count + 1,))
        seconds.start()

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        f"wss://ws.finnhub.io?token={api_key}",
        on_open=on_open,
        on_message=on_message,
        on_close=on_close
    )

    timer = threading.Timer(10, stop_ws)
    timer.start()

    print("running")
    second_count(1)

    ws.run_forever()

