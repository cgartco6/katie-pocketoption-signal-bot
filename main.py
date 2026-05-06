import asyncio
import pandas as pd
import ccxt
from dotenv import load_dotenv
import os
from config import *
from indicators import calculate_indicators, is_bearish_signal
from telegram_bot import send_signal

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

exchange = ccxt.binance()  # Or use forex-specific source (e.g., fxcmpy, or Pocket-friendly API)
bot = Bot(token=TELEGRAM_TOKEN)

async def main_loop():
    print("Katie Bot Started - Sending continuous signals...")
    while True:
        for pair in MAJOR_PAIRS:
            try:
                ohlcv = exchange.fetch_ohlcv(pair.replace('/', ''), TIMEFRAME, limit=LIMIT)
                df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                
                df = calculate_indicators(df)
                result = is_bearish_signal(df)
                
                if result['signal']:
                    await send_signal(bot, TELEGRAM_CHAT_ID, pair, result)
                    print(f"Signal sent for {pair}")
            except Exception as e:
                print(f"Error on {pair}: {e}")
        
        await asyncio.sleep(30)  # Check frequently for near-real-time signals (before candle close)

if __name__ == "__main__":
    asyncio.run(main_loop())
