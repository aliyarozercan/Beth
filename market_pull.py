# market_pull.py

from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os

def get_market_summary():
    # API key should be set via environment variable for security
    CMC_API_KEY = os.getenv("CMC_API_KEY", "your-api-key-here")
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '10',
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = response.json()

        tracked = ["Bitcoin", "Ethereum", "Solana"]
        output = "📈 Crypto Market Summary (CoinMarketCap):\n"

        for coin in data.get("data", []):
            name = coin.get("name")
            if name not in tracked:
                continue
            price = coin["quote"]["USD"]["price"]
            change = coin["quote"]["USD"]["percent_change_24h"]
            emoji = "📉" if change < 0 else "📈"
            output += f"{emoji} {name}: ${price:,.2f} ({change:+.2f}%) in last 24h\n"

        return output.strip()

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return f"Error fetching market data: {e}"

if __name__ == "__main__":
    print(get_market_summary())
