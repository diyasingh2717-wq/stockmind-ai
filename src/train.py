# src/train.py

import joblib
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error
from .data_fetch import fetch_data
from .features import add_indicators
from .labels import create_labels
from config import TEST_SIZE_RATIO, RANDOM_STATE
import numpy as np

def train_models():

    df = fetch_data()
    df = add_indicators(df)
    df = create_labels(df)

    features = [
        "RSI", "EMA20", "EMA50", "EMA200",
        "MACD", "MACD_signal", "ATR", "Volume_Change"
    ]

    X = df[features].copy()

# 🔥 Replace infinite values
    X.replace([np.inf, -np.inf], np.nan, inplace=True)

# 🔥 Drop rows with NaN
    X.dropna(inplace=True)

# Align targets after dropping rows
    y_class = df.loc[X.index, "Trend"]
    y_up = df.loc[X.index, "Up_Move"]
    y_down = df.loc[X.index, "Down_Move"]

    split = int(len(df) * (1 - TEST_SIZE_RATIO))

    X_train = X[:split]
    X_test = X[split:]

    y_class_train = y_class[:split]
    y_class_test = y_class[split:]

    y_up_train = y_up[:split]
    y_up_test = y_up[split:]

    y_down_train = y_down[:split]
    y_down_test = y_down[split:]

    clf = RandomForestClassifier(
        n_estimators=200,
        random_state=RANDOM_STATE
    )

    clf.fit(X_train, y_class_train)

    reg_up = RandomForestRegressor(
        n_estimators=200,
        random_state=RANDOM_STATE
    )

    reg_down = RandomForestRegressor(
        n_estimators=200,
        random_state=RANDOM_STATE
    )

    reg_up.fit(X_train, y_up_train)
    reg_down.fit(X_train, y_down_train)

    print("Accuracy:",
          accuracy_score(y_class_test,
                         clf.predict(X_test)))

    print("UP Model MAE:",
      mean_absolute_error(y_up_test,
                          reg_up.predict(X_test)))

    print("DOWN Model MAE:",
        mean_absolute_error(y_down_test,
                          reg_down.predict(X_test)))

    joblib.dump(clf, "models/trend_model.pkl")
    joblib.dump(reg_up, "models/up_model.pkl")
    joblib.dump(reg_down, "models/down_model.pkl")


if __name__ == "__main__":
    train_models()