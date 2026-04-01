import ssl
import certifi
ssl._create_default_https_context = ssl.create_default_context(cafile=certifi.where())

import yfinance as yf

def predict(stock):
    try:
        data = yf.download(stock, period="30d", interval="1d", progress=False)

        if data.empty:
            raise ValueError(f"No data for '{stock}'")

        close = data["Close"].squeeze()

        if len(close) < 5:
            raise ValueError("Not enough data to predict.")

        last = float(close.iloc[-1])
        prev = float(close.iloc[-2])
        returns = close.pct_change().dropna()

        trend = "UP" if last > prev else "DOWN"

        if trend == "UP":
            consistency = float((returns > 0).sum() / len(returns))
        else:
            consistency = float((returns < 0).sum() / len(returns))

        probability = round(max(0.51, min(0.92, consistency)), 2)
        target_price = last * (1.01 if trend == "UP" else 0.99)

        return trend, probability, target_price

    except Exception as e:
        raise e