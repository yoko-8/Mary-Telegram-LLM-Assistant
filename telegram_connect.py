import logging
from telegram import Update, ForceReply
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CommandHandler
import os
from dotenv import load_dotenv

from api_connect2 import generate
from module_engine.prompt_classifier import classify_user_input
from memory_module.brain import remember_memories, save_memories
from weather_module.weather import get_weather, read_location, write_location
from calendar_module.google_cal import get_calendar_events

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
USER_ID = os.getenv("USER_ID")

# Enable logging in Python terminal
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def set_location_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    write_location(update.message.text[13:])
    await update.message.reply_text("Your location has been updated as: " + read_location())


async def current_location_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Your current location is: " + read_location())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_message = ("Hey boss! Here's some commands you can use.\n"
                    "/setlocation - Set your location, i.e. \"New York\"\n"
                    "/currentlocation - Your currently set location")
    await update.message.reply_text(help_message)


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.message.text

    if update.effective_chat.id != USER_ID or update.message.chat.type != 'private':
        await update.message.reply_text("You're not boss! Get outta here!")
    else:
        module = classify_user_input(query)
        if module == "Calendar":
            cal_events = get_calendar_events(query) # This needs to be stringified
            recent_mems = None # need to grab recent memories from memory_module
            response = generate(cal_events, recent_mems, query)
            await update.message.reply_text(response)
        elif module == "Weather":
            weather = get_weather(query) # This needs to be stringified
            recent_mems = None # need to grab recent memories from memory_module. max 2048
            response = generate(weather, recent_mems, query)
            await update.message.reply_text(response)
        elif module == "Chat":
            related_mems = remember_memories(query)
            recent_mems = None # need to grab recent memories from memory_module
            response = generate(related_mems, recent_mems, query)
            await update.message.reply_text(response)


def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # commands
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("setlocation", set_location_command))
    application.add_handler(CommandHandler("currentlocation", current_location_command))

    # chat functionality
    application.add_handler(MessageHandler(filters.TEXT & ~filters.LOCATION, chat))

    # run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
