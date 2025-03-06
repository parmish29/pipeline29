from nsepython import *
import gspread
import pandas as pd
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import time

# 🔹 Google Sheets API Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credex.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Forex_Data").sheet1  # Change to your Google Sheet name

# 🔹 NSE Stocks List (40 stocks)
stocks = [
    "RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "LT", "BHARTIARTL",
    "ITC", "KOTAKBANK", "TITAN", "BAJFINANCE", "ONGC", "HCLTECH", "MARUTI", "WIPRO",
    "ASIANPAINT", "ADANIPORTS", "ULTRACEMCO", "POWERGRID", "TECHM", "TATAMOTORS", 
    "SUNPHARMA", "NTPC", "JSWSTEEL", "HINDUNILVR", "GRASIM", "COALINDIA", "BPCL",
    "BRITANNIA", "HINDALCO", "EICHERMOT", "DIVISLAB", "DRREDDY", "INDUSINDBK", 
    "NESTLEIND", "UPL", "TATASTEEL", "IOC", "M&M"
]

# 🔹 Fetch and Store Data in Columns
def fetch_and_store_stock_data():
    try:
        # 🔹 Get all stock prices
        prices = []
        for stock in stocks:
            try:
                prices.append(nse_quote_ltp(stock))
                print(f"✅ {stock}: {prices[-1]}")
            except Exception as e:
                prices.append("N/A")  # Store 'N/A' for errors
                print(f"❌ Error fetching {stock}: {e}")

        # 🔹 Get current time as column header (Date + Hour)
        column_name = datetime.now().strftime("%Y-%m-%d %H:%M")

        # 🔹 Get current sheet data
        existing_data = sheet.get_all_values()
        headers = existing_data[0] if existing_data else []

        # 🔹 If new column header doesn't exist, add it
        if column_name not in headers:
            sheet.update_cell(1, len(headers) + 2, column_name)  # Append new column

        # 🔹 Find the correct column index
        col_index = headers.index(column_name) + 2 if column_name in headers else len(headers) + 2

        # 🔹 Append stock prices in respective rows (starting from row 2)
        cell_range = f"{chr(64 + col_index)}2:{chr(64 + col_index)}{len(stocks) + 1}"
        sheet.update(cell_range, [[p] for p in prices], value_input_option="USER_ENTERED")

        print(f"✅ Data updated at {datetime.now().strftime('%H:%M')} in column {column_name}")

    except Exception as e:
        print(f"❌ Google Sheets Update Failed: {e}")

# 🔹 Run the Pipeline Every 5 Minutes
while True:
    fetch_and_store_stock_data()
    time.sleep(300)  # 5 minutes
