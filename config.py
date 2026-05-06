MAJOR_PAIRS = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'AUD/USD', 'USD/CAD', 'USD/CHF', 'NZD/USD']  # Adjust format per data source
TIMEFRAME = '1m'
LIMIT = 300  # candles to fetch

# Strategy params (exact from Katie)
EMA_FAST = 3
EMA_SLOW = 10
VORTEX_LENGTH = 10
MACD_FAST = 15
MACD_SLOW = 27
MACD_SIGNAL = 9

TELEGRAM_TOKEN = None  # Loaded from .env
TELEGRAM_CHAT_ID = None
