import pandas as pd
import pandas_ta as ta

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df['ema3'] = ta.ema(df['close'], length=3)
    df['ema10'] = ta.ema(df['close'], length=10)
    
    vortex = ta.vortex(df['high'], df['low'], df['close'], length=10)
    df['vi_plus'] = vortex['VIp_10']
    df['vi_minus'] = vortex['VIm_10']
    
    macd = ta.macd(df['close'], fast=15, slow=27, signal=9)
    df = pd.concat([df, macd], axis=1)
    return df

def is_bearish_signal(df: pd.DataFrame, max_macd_candles=4) -> dict:
    if len(df) < 50:
        return {'signal': False, 'reason': 'Not enough data'}
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    prev2 = df.iloc[-3] if len(df) > 2 else prev
    
    # EMA cross / alignment
    ema_down = (prev['ema3'] > prev['ema10'] and latest['ema3'] <= latest['ema10']) or latest['ema3'] < latest['ema10']
    
    # Vortex bearish
    vortex_bear_cross = (prev['vi_plus'] > prev['vi_minus'] and latest['vi_plus'] <= latest['vi_minus'])
    vortex_bear = vortex_bear_cross or latest['vi_minus'] > latest['vi_plus']
    
    # MACD bearish + freshness
    macd_hist_down = latest['MACDh_15_27_9'] < 0
    macd_cross = latest['MACDs_15_27_9'] < prev['MACDs_15_27_9']
    # Rough freshness check (count recent down histogram bars)
    recent_down = sum(1 for i in range(1, max_macd_candles+2) if df['MACDh_15_27_9'].iloc[-i] < 0)
    fresh = recent_down <= max_macd_candles + 1
    
    candle_red = latest['close'] < latest['open']
    
    strong_signal = ema_down and vortex_bear and macd_hist_down and fresh
    
    return {
        'signal': strong_signal,
        'direction': 'DOWN (PUT)',
        'strength': 'HIGH' if (strong_signal and candle_red) else 'MEDIUM',
        'details': f"EMA3:{latest['ema3']:.5f} EMA10:{latest['ema10']:.5f} | VI-:{latest['vi_minus']:.3f} VI+:{latest['vi_plus']:.3f} | MACD Hist:{latest['MACDh_15_27_9']:.5f} | Red Candle: {candle_red}"
    }
