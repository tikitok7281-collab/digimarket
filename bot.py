"""
DigiMarket Telegram bot — deep-link MVP for @DigiMarketStoreBot.
Python 3.11+, aiogram 3.x

Set BOT_TOKEN and WEBAPP_URL as environment variables.
Never commit BOT_TOKEN to source control.
"""
import os, asyncio, logging
from pathlib import Path
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup,
    InlineKeyboardButton, WebAppInfo, FSInputFile
)

TOKEN = os.environ["BOT_TOKEN"]
WEBAPP_URL = os.environ.get("WEBAPP_URL", "https://YOUR-HTTPS-MINI-APP-URL.example")
BOT_USERNAME = "DigiMarketStoreBot"

bot = Bot(TOKEN)
dp = Dispatcher()
ROOT = Path(__file__).parent

PRODUCTS = {
    "avito_pack": {
        "title": "Avito Master — стартовый набор",
        "description": "PDF-шаблоны и таблица-калькулятор для продавцов. Цифровой товар.",
        "stars": 100,  # TEST PRICE ONLY: choose final Stars price before launch.
        "files": [
            "products/Avito_Master_starter_kit.pdf",
            "products/Avito_Master_profit_calculator.xlsx",
        ],
    }
}

async def send_invoice(chat_id: int, product_id: str):
    product = PRODUCTS.get(product_id)
    if not product:
        await bot.send_message(chat_id, "Такого товара пока нет в каталоге.")
        return
    await bot.send_invoice(
        chat_id=chat_id,
        title=product["title"],
        description=product["description"],
        payload=f"product:{product_id}",
        provider_token="",  # Required empty provider token for Telegram Stars.
        currency="XTR",
        prices=[LabeledPrice(label=product["title"], amount=product["stars"])],
    )

@dp.message(CommandStart(deep_link=True))
async def start(message: Message, command):
    payload = command.args or ""
    if payload.startswith("buy_"):
        await send_invoice(message.chat.id, payload.removeprefix("buy_"))
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Открыть DigiMarket",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    ]])
    await message.answer(
        "Добро пожаловать в DigiMarket ✦\n"
        "Каталог цифровых продуктов и полезных инструментов.\n\n"
        "Нажми кнопку, чтобы открыть магазин.",
        reply_markup=keyboard
    )

@dp.message(Command("paysupport"))
async def paysupport(message: Message):
    await message.answer(
        "Поддержка по оплате и возвратам: ДОБАВИТЬ_КОНТАКТ_ВЗРОСЛОГО_ВЛАДЕЛЬЦА"
    )

@dp.message(Command("catalog"))
async def catalog(message: Message):
    await message.answer(
        "Наш первый продукт:\n"
        "Avito Master — стартовый набор.\n"
        "Для покупки нажми: /buy_avito_pack"
    )

@dp.message(Command("buy_avito_pack"))
async def buy_avito_pack(message: Message):
    await send_invoice(message.chat.id, "avito_pack")

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    payload = query.invoice_payload
    product_id = payload.removeprefix("product:")
    if product_id not in PRODUCTS:
        await query.answer(ok=False, error_message="Товар больше недоступен.")
        return
    await query.answer(ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message: Message):
    payment = message.successful_payment
    product_id = payment.invoice_payload.removeprefix("product:")
    product = PRODUCTS.get(product_id)
    if not product:
        await message.answer(
            "Платёж получен, но товар не найден. Пожалуйста, обратись в поддержку."
        )
        return

    # TODO before public launch: store payment/order records in a persistent database,
    # protect against duplicate delivery, implement refunds and file recovery.
    await message.answer("Оплата прошла успешно! Вот твой цифровой товар:")
    for relative_path in product["files"]:
        file_path = ROOT / relative_path
        if file_path.exists():
            await message.answer_document(FSInputFile(file_path))
        else:
            await message.answer(
                "Один из файлов временно недоступен. Напиши в поддержку."
            )

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
