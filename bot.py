import os
import random
import sqlite3
import time
from datetime import date
from aiohttp import web

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (Message, CallbackQuery, ReplyKeyboardMarkup, 
                           KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# --- НАСТРОЙКИ ---
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Берем из настроек Render
ADMIN_PASSWORD = "admin123" 
WEBHOOK_URL = os.getenv("WEBHOOK_URL") # Ссылка от Render

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# ---------- БД ----------
conn = sqlite3.connect("hypergram.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY, username TEXT, region TEXT, number TEXT,
    balance INTEGER DEFAULT 0, last_bonus TEXT
)
""")
cur.execute("PRAGMA table_info(users)")
columns = [row[1] for row in cur.fetchall()]
if "is_admin" not in columns:
    cur.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
if "blocked_until" not in columns:
    cur.execute("ALTER TABLE users ADD COLUMN blocked_until INTEGER DEFAULT 0")
if "wrong_attempts" not in columns:
    cur.execute("ALTER TABLE users ADD COLUMN wrong_attempts INTEGER DEFAULT 0")
conn.commit()

SPECIAL = {"Dofamiiin4ik": "+888 000", "aarchang3l": "+888 888", "Sram_gyt": "+888 888 888"}

class AdminStates(StatesGroup):
    waiting_password = State()
    waiting_target_id = State()
    waiting_amount = State()
    waiting_broadcast = State()

# ... (ВСЕ ФУНКЦИИ И ХЕНДЛЕРЫ ИЗ ПРЕДЫДУЩЕГО КОДА) ...

# ⚠️ ВАЖНО: Вставьте сюда ВСЕ ваши функции и хендлеры из прошлого кода
# (get_user, save_region, gen_number, все клавиатуры и @dp.message/@dp.callback_query)
# Я не буду дублировать их здесь, чтобы не раздувать сообщение. 
# Просто скопируйте их из вашего текущего файла bot.py.

# --- ЗАПУСК ЧЕРЕЗ ВЕБХУК ---
async def on_startup(bot: Bot):
    await bot.set_webhook(f"{WEBHOOK_URL}/webhook")

async def main():
    dp.startup.register(on_startup)
    
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    
    # Render сам назначает порт через переменную окружения PORT
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
