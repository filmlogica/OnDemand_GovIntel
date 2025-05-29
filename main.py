import os
import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the Finnhub API key from the .env file
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

if not FINNHUB_API_KEY:
    raise ValueError("Missing FINNHUB_API_KEY in .env file")

# Load indexes.csv from the same folder as this script
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, 'indexes.csv')

# Read the stock symbols
try:
    df = pd.read_csv(csv_path)
    symbols = df['symbol'].dropna().tolist()
except Exception as e:
    raise FileNotFoundError(f"Could not read {csv_path}: {e}")

# Call Finnhub API for each symbol
def fetch_stock_data(symbol):
    url = f'https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f"Failed to fetch {symbol} (HTTP {response.status_code})"}

# Run the query loop
def main():
    for symbol in symbols:
        print(f"Fetching data for: {symbol}")
        data = fetch_stock_data(symbol)
        print(data)

if __name__ == '__main__':
    main()
