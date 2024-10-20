import yfinance as yf

def get_data(symbol='AAPL',period='1mo'):
    ticker_symbol = symbol
    ticker = yf.Ticker(ticker_symbol)
    historical_data = ticker.history(period=period)
    return historical_data
