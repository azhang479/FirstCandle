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
import sys

#dataset of candles {ticker:{Candles}}
dataset = {}
tick = True
currentMinute = -1

#initialize the client
load_dotenv()
api_key = os.getenv("API_KEY")
finnhub_client = finnhub.Client(api_key)

#prints out the message from the websocket
def on_message(ws, message):
    global dataset
    global currentMinute

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
            f_hour = f"{hour:02d}"
            f_minute = f"{minute:02d}"
            index = f"{f_hour}:{f_minute}"
            if (currentMinute == -1):
                currentMinute = minute

            tickerDict = dataset.get(ticker)

            if (index in dataset.get(ticker)):
                cand = tickerDict.get(index)
                cand.updateCandle(price, volume)
            else:
                tickerDict[index] = Candle(minute, 1, price, volume)
            
            if (minute != currentMinute):
                index = f"{f_hour}:{((minute - 1) % 60):02d}"
                currentMinute = minute
                tickerDict.get(index).closeCandle()


#what to subscribe to when opening the websocket
def on_open(ws):
    global dataset
    global tick
    tickers = ["BINANCE:BTCUSDT", "NVDA"]
    for ticker in tickers:
        print(f"Connecting to {ticker}")
        ws.send(json.dumps({"type": "subscribe", "symbol": ticker}))
        dataset.update({ticker:{}})

    #start counter after we connect
    secondCount(1)
    timer = threading.Timer(length, stop_ws)
    timer.start()


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
        if (tickerDict):
            tickerDict.get(list(tickerDict)[0]).setUnusable()
            tickerDict.get(list(tickerDict)[-1]).setUnusable()

    tick = False
    print(dataset)
    ws.close()


"""
Ticker function to tick each second for tracking purposes
"""
def secondCount(count):
    if (tick):
        print(count)
        seconds = threading.Timer(1, secondCount, args=(count + 1,))
        seconds.start()


"""
Consolidates multiple candles into a larger candle

Input:
-- ticker: The ticker of the candles you'd like to look at
-- hour/minute: The beginning of the consolidation taken from (f"{hour:02d}:{minute:02d}") format
-- timeFrame: Number of minutes to consolidate
Output:
-- The OHLCV of the consolidated candle

If any candle is unusable, it will be replaced with the nearest useable candle.
If none exists all return values will be -1.
Use: consolidateCandles("AAPL", '09:30', 5) will give a 5 minute candle starting at 09:30.
"""
def consolidateCandles(ticker, hour, minute, timeFrame):
    tickerDict = dataset.get(ticker)
    if(not tickerDict):
        return None
    
    index = f"{hour}:{(minute)}"
    firstCandle = tickerDict.get(index)
    if (not firstCandle):
        return None
    
    data = firstCandle.exportCandleInfo
    print(data)

    return None

    Cand = Candle()
    for i in range(timeFrame):
        index = f"{hour}:{(minute + i + 1) % 60}"
    dataset[ticker]
    c_open = 0
    c_high = 0
    c_low = 0
    c_close = 0
    c_volume = 0

if __name__ == "__main__":
    length = 10
    ws = websocket.WebSocketApp(
        f"wss://ws.finnhub.io?token={api_key}",
        on_open=on_open,
        on_message=on_message,
        on_close=on_close
    )

    if len(sys.argv) > 1:
        length = int(sys.argv[1])

    print("running")
    ws.run_forever()


