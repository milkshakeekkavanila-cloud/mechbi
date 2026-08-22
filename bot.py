"""
Simple Telegram Chatbot using python-telegram-bot (v20+, async).

Setup:
1. Message @BotFather on Telegram, run /newbot, and copy the token it gives you.
2. Set that token as an environment variable named TELEGRAM_BOT_TOKEN
   (or paste it directly where noted below, though env vars are safer).
3. pip install -r requirements.txt
4. python bot.py
"""

import logging
import os

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# --- Configuration ---------------------------------------------------------

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "PASTE_YOUR_TOKEN_HERE")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# --- Command handlers --------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm alive. Send me a message, or try /help."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /help command."""
    await update.message.reply_text(
        "Commands:\n"
        "/start - greet the bot\n"
        "/help - show this message\n\n"
        "Anything else you type gets echoed back. "
        "Edit the echo() function in bot.py to change that behavior."
    )


# --- Message handler ---------------------------------------------------------

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echoes any non-command text message back to the user.

    Replace the body of this function to add real logic — e.g. call an
    API, look something up, run a calculation, etc.
    """
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")


# --- Error handler ------------------------------------------------------------

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Update %s caused error %s", update, context.error)


# --- Entry point ---------------------------------------------------------------

def main() -> None:
    if BOT_TOKEN == "PASTE_YOUR_TOKEN_HERE":
        raise SystemExit(
            "No bot token found. Set the TELEGRAM_BOT_TOKEN environment variable "
            "or edit BOT_TOKEN in bot.py."
        )

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_error_handler(error_handler)

    logger.info("Bot starting... Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
