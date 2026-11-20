# DigiMarket MVP for @DigiMarketStoreBot

This is a starter package. It is not deployed and is not ready for public payments until the checklist below is completed.

## Included
- `index.html` — responsive catalog / Telegram Mini App front-end.
- `bot.py` — aiogram 3 bot with `/start`, deep-link purchase, Telegram Stars invoice and file delivery.
- `products/` — Avito Master PDF and XLSX.

## 1. BotFather setup
Use `/setdescription` for a short description, `/setabouttext` for the profile text, and `/setcommands` with:
start - Открыть DigiMarket
catalog - Посмотреть каталог
buy_avito_pack - Купить Avito Master
paysupport - Поддержка по оплате

Do not set the Mini App URL until the site is deployed on HTTPS.

## 2. Hosting
Upload `index.html` to a static host with HTTPS. Upload the full project to a trusted Python host for the bot. Keep the product files on the bot server (not public web root).

## 3. Environment
Set `BOT_TOKEN` securely in the hosting provider's environment variables.
Set `WEBAPP_URL` to the deployed HTTPS address of `index.html`.
Never put the bot token in source code, frontend HTML, screenshots, or chat.

## 4. Run
Python 3.11+
`pip install -r requirements.txt`
`python bot.py`

## 5. Payments and compliance
Telegram requires Telegram Stars (`XTR`) for digital goods sold inside bots and Mini Apps. Official documentation:
https://core.telegram.org/bots/payments-stars
https://core.telegram.org/bots/webapps

The price `100` in `bot.py` is a placeholder in Stars, not a ruble amount. Choose a final price and test the purchase/refund flow. Add a real support contact to `/paysupport`.

Since the project owner is under 18, ask a parent/legal representative to review account ownership, payout eligibility, tax, consumer rights, refunds and platform terms before accepting money.

## 6. Still required before public launch
- Persistent database for orders and Telegram `telegram_payment_charge_id`.
- Duplicate-payment and duplicate-delivery protection.
- Refund flow and `/paysupport` handling.
- Purchase recovery if user loses the file.
- Admin-only product management.
- Logging, backups, rate limiting and error alerts.
- Verify Telegram Stars availability/payout conditions for the relevant account and region.
- End-to-end tests in a private test group before sharing publicly.

This MVP is not a promise of sales or passive income. It automates payment delivery after deployment; acquiring customers still needs a plan.
