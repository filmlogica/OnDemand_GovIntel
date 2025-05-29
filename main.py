import os
import csv
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="/home/roymnel/Documents/OnDemand_GovIntel/.env")

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
CSV_PATH = "/home/roymnel/Documents/OnDemand_GovIntel/indexes.csv"
OUTPUT_PATH = "/home/roymnel/Documents/OnDemand_GovIntel/summary_results.txt"

# Get stock symbols from CSV
def get_stock_symbols(filepath):
    symbols = []
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # avoid empty lines
                symbols.append(row[0].strip().upper())
    return symbols

# Fetch data from Finnhub
def fetch_finnhub_data(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Query the LLM for analysis
def query_llm(symbol, data):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "You are a financial analyst."},
            {"role": "user", "content": f"Analyze stock {symbol} with this data: {data}. Provide an investment insight."}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

# Main loop
def main():
    symbols = get_stock_symbols(CSV_PATH)
    results = []

    for symbol in symbols:
        try:
            data = fetch_finnhub_data(symbol)
            summary = query_llm(symbol, data)
            entry = f"\n--- {symbol} ---\n{summary}\n"
            print(entry)
            results.append(entry)
        except Exception as e:
            error_msg = f"\n--- {symbol} ---\nError: {str(e)}\n"
            print(error_msg)
            results.append(error_msg)

    # Save to file
    with open(OUTPUT_PATH, "w") as f:
        f.writelines(results)

if __name__ == "__main__":
    main()

