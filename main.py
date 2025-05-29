import yfinance as yf
import pandas as pd
import os

# Load symbols from indexes.csv
csv_path = os.path.join(os.path.dirname(__file__), "indexes.csv")
symbols = pd.read_csv(csv_path)['symbol'].dropna().tolist()

# Create or clear output file
with open("stock_data.txt", "w") as output_file:
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            output_file.write(f"--- {symbol} ---\n")
            output_file.write(f"Name: {info.get('longName', 'N/A')}\n")
            output_file.write(f"Price: {info.get('regularMarketPrice', 'N/A')}\n")
            output_file.write(f"Sector: {info.get('sector', 'N/A')}\n")
            output_file.write("\n")
        except Exception as e:
            output_file.write(f"Failed to fetch {symbol}: {e}\n\n")
