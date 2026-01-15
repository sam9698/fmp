#!/usr/bin/env python3
import os, time, datetime as dt, requests, json

FMP_KEY   = os.getenv("FMP_KEY")                # supplied by GitHub secret
WEBHOOK   = "https://hook.k1m1.ai/us30"         # I receive here
SYMBOL    = "US30"
INTERVAL  = "1min"
URL       = f"https://financialmodelingprep.com/api/v3/historical-chart/{INTERVAL}/{SYMBOL}?apikey={FMP_KEY}"

def latest_bar():
    """Return newest 1-min bar from FMP."""
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    data = r.json()          # newest bar first
    return data[0]           # dict with open, high, low, close, volume, date

def post_to_k1m1(bar):
    payload = {
        "symbol": SYMBOL,
        "open"  : float(bar["open"]),
        "high"  : float(bar["high"]),
        "low"   : float(bar["low"]),
        "close" : float(bar["close"]),
        "volume": int(bar["volume"]),
        "time"  : bar["date"]
    }
    resp = requests.post(WEBHOOK, json=payload, timeout=10)
    print(dt.datetime.utcnow(), resp.status_code, resp.text[:100])

if __name__ == "__main__":
    while True:                       # loop forever
        try:
            post_to_k1m1(latest_bar())
        except Exception as e:
            print("err", e)
        time.sleep(60)                # next bar