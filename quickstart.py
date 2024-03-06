import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from instascrape import Reel
import time

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="please help me")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


async def insta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    SESSIONID = "18912d60af9-f3fe62"

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
    "cookie":f'sessionid={SESSIONID};'
    }
    
    insta_reel = Reel("https://www.instagram.com/reel/CtzQXdrAjqc/?utm_source=ig_web_copy_link&igshid=MzRlODBiNWFlZA==")
    insta_reel.scrape(headers=headers)
    # reel_path = f"assets/insta/{int(time.time())}.mp4"
    # insta_reel.download(fp=f"assets/insta/{int(time.time())}.mp4")
    # text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"This reel has {insta_reel.video_view_count:,} views.")
    # await context.bot.send_video(chat_id=update.effective_chat.id, video=open(reel_path, "rb"))

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

if __name__ == '__main__':
    application = ApplicationBuilder().token('6330688279:AAHISlrS4cNEj8OBr8B9ivBekWeIGt7bufI').build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    caps_handler = CommandHandler('caps', caps)
    insta_handler = CommandHandler('insta', insta)


    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(help_handler)
    application.add_handler(caps_handler)
    application.add_handler(insta_handler)

    application.add_handler(unknown_handler)
    
    
    application.run_polling()