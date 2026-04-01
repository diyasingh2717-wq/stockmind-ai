# config.py
Stock_Name=input("Enter Your Stock Name: ")

# Stock settings
STOCK_SYMBOL = Stock_Name+".NS"
PERIOD = "10y"
INTERVAL = "1d"

# Prediction settings
FUTURE_DAYS = 1

# Model settings
TEST_SIZE_RATIO = 0.2
RANDOM_STATE = 42