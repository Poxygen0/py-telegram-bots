import logging
import os
from typing import Optional
from dotenv import load_dotenv
from telegram import Update, ChatJoinRequest
from telegram.ext import Application, ChatJoinRequestHandler, ContextTypes

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))


# ===== Logging Setup =====

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Format logs
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Suppress noisy logs from httpx (used by PTB)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


# ===== Bot Logic =====

_pending: list[ChatJoinRequest] = []

async def join_request_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Buffer incoming join requests and schedule a batch approval.
    """
    req = update.chat_join_request
    _pending.append(req)
    logger.info("Buffered join request from user_id=%s", req.from_user.id)

    if len(_pending) == 1:
        # Schedule batch approval in 60 seconds
        context.job_queue.run_once(_approve_pending, when=60, name="batch_join_approve")


async def _approve_pending(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Approve all buffered join requests, send welcome PMs, and log outcomes.
    """
    bot = context.bot
    to_approve = list(_pending)
    _pending.clear()

    for req in to_approve:
        try:
            await bot.approve_chat_join_request(chat_id=req.chat.id, user_id=req.from_user.id)
            logger.info("Approved join request for user_id=%s", req.from_user.id)
        except Exception as e:
            logger.error("Failed to approve join request for user_id=%s: %s", req.from_user.id, e)
            continue

        if req.user_chat_id:
            try:
                await bot.send_message(
                    chat_id=req.user_chat_id,
                    text=(f"Welcome to **{req.chat.title or req.chat.id}**, {req.from_user.first_name}!"),
                    parse_mode="Markdown",
                )
                logger.info("Sent welcome PM to user_id=%s", req.from_user.id)
            except Exception as e:
                logger.error("Could not send PM to user_id=%s: %s", req.from_user.id, e)


# ===== Global Error Handler =====

async def error_handler(update: Optional[object], context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle all uncaught exceptions from handlers.

    Logs the error and optionally notifies a developer/admin via Telegram.
    """
    err = context.error
    logger.exception("Unhandled exception occurred: %s", err)

    # Optionally notify a owner
    try:
        await context.bot.send_message(
            chat_id=OWNER_ID,
            text=f"⚠️ Bot error: <code>{err}</code>",
            parse_mode="HTML",
        )
    except Exception as notify_error:
        logger.error("Failed to send error notification: %s", notify_error)


# ===== Main =====

def main() -> None:
    """
    Start the Telegram bot.
    """
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(ChatJoinRequestHandler(join_request_handler))
    app.add_error_handler(error_handler)

    logger.info("Starting bot polling …")
    app.run_polling(allowed_updates=["chat_join_request"])
    logger.info("Bot stopped.")


if __name__ == "__main__":
    main()
