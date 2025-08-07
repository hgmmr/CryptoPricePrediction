from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

# 🔐 এখানে তোমার BotFather থেকে পাওয়া বট টোকেন বসাও
BOT_TOKEN = "8167532083:AAEthFJ_iywqADFYut56k0DLzPiuDe2MgR0"

# 🔍 বর্তমান দাম খোঁজার ফাংশন
def get_price(coin):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin}&vs_currencies=usd"
    res = requests.get(url)
    data = res.json()
    return data.get(coin, {}).get('usd', None)

# 📊 মার্কেট ইতিহাস (৭ দিনের)
def get_market_chart(coin, days=7):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days={days}"
    res = requests.get(url)
    data = res.json()
    prices = [p[1] for p in data['prices']]
    return prices

# 🔮 প্রেডিকশন (Simple Moving Average)
def predict_price(prices):
    return sum(prices) / len(prices)

# 📌 /price কমান্ড হ্যান্ডলার
async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("দয়া করে টোকেনের নাম লিখুন। উদাহরণ: /price bitcoin")
        return

    coin = context.args[0].lower()
    price = get_price(coin)

    if price:
        await update.message.reply_text(f"💰 {coin.capitalize()} এর বর্তমান দাম: ${price}")
    else:
        await update.message.reply_text("❌ টোকেন পাওয়া যায়নি!")

# 📌 /predict কমান্ড হ্যান্ডলার
async def predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("দয়া করে টোকেনের নাম লিখুন। উদাহরণ: /predict ethereum")
        return

    coin = context.args[0].lower()
    prices = get_market_chart(coin)

    if prices:
        predicted = predict_price(prices)
        await update.message.reply_text(f"🔮 {coin.capitalize()} এর ৭ দিনের গড় দাম (Simple Prediction): ${predicted:.2f}")
    else:
        await update.message.reply_text("❌ টোকেনের ইতিহাস পাওয়া যায়নি!")

# 📌 /start কমান্ড হ্যান্ডলার
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 স্বাগতম! আমি একটি ক্রিপ্টো প্রাইস প্রেডিকশন বট।\n\n"
        "🔎 /price [coin] → বর্তমান দাম দেখুন\n"
        "🔮 /predict [coin] → প্রেডিকশন দেখুন"
    )

# ▶️ বট চালু করার মেইন ফাংশন
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("price", price_command))
    app.add_handler(CommandHandler("predict", predict_command))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
                      main()
