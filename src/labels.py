# src/labels.py

import numpy as np
from config import FUTURE_DAYS


def create_labels(df):
    """
    Create classification and regression targets
    """

    # Future close price
    df["Future_Close"] = df["Close"].shift(-FUTURE_DAYS)

    # Classification label
    df["Trend"] = np.where(
        df["Future_Close"] > df["Close"],
        1,
        0
    )

    # Future max price
# Future highest price
    df["Future_Max"] = (
        df["High"]
        .rolling(FUTURE_DAYS)
        .max()
        .shift(-FUTURE_DAYS)
    )

# Future lowest price
    df["Future_Min"] = (
        df["Low"]
        .rolling(FUTURE_DAYS)
        .min()
        .shift(-FUTURE_DAYS)
    )

# Upside move
    df["Up_Move"] = df["Future_Max"] - df["Close"]

# Downside move
    df["Down_Move"] = df["Close"] - df["Future_Min"]
    df.dropna(inplace=True)

    return df