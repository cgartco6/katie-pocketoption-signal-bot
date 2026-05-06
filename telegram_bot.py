from telegram import Bot
import asyncio

async def send_signal(bot: Bot, chat_id: str, pair: str, signal: dict):
    msg = f"""🚨 **KATIE STRATEGY SIGNAL** (Live)
Pair: **{pair}**
Direction: **{signal['direction']}** | 1min expiry
Strength: **{signal['strength']}**
{signal['details']}
Time: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
Test on DEMO first!"""
    await bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')
