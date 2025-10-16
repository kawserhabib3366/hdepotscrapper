"""
Improved Telegram bot for processing a list of items per chat and running background tasks.
- Uses environment variable for BOT_TOKEN (no hard-coded token)
- Deletes any webhook before starting polling to avoid Conflict
- Uses context.application.create_task to attach background tasks to the app loop
- Uses locks to prevent concurrent changes to a chat's item list while processing
- Graceful cancellation and cleanup of tasks
- Logging and error handling
- Additional helper commands: /add, /list, /clear, /help

Drop-in replacement for your original script. Edit get_all_store_price call as needed.
"""

import os
import sys
import requests
import asyncio
import logging
from typing import Dict, List

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram.error import Conflict

# Replace this import with your actual implementation
from check_price import get_all_store_price

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# In-memory per-chat state
user_tasks: Dict[int, asyncio.Task] = {}
user_items: Dict[int, List[str]] = {}
user_locks: Dict[int, asyncio.Lock] = {}

# Constants
DEFAULT_ITEM_DELAY = 2  # seconds between items
MAX_RETRIES = 2


def get_bot_token() -> str:
    token = os.environ.get("BOT_TOKEN")
    token = "7209908346:AAGUKR0abafZ8ddkAUTclg8qpysEB9-h0dk"

    if not token:
        logger.error("BOT_TOKEN environment variable is not set. Exiting.")
        raise SystemExit("Set BOT_TOKEN environment variable")
    return token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Send me the list of items (one per line) and then press /run to start the task.\n"
        "You can also use /add to add items, /list to show current items, /clear to remove them."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/start - Usage instructions\n"
        "/run - Start processing your items\n"
        "/stop - Stop the processing task\n"
        "/status - Check if a task is running\n"
        "/add - Add item(s) (one per line) as a message\n"
        "/list - Show current items\n"
        "/clear - Remove current items\n"
    )


async def receive_items(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Receive free-text items and replace the current list for the chat.
    If you want to add items, use /add command instead."""
    chat_id = update.effective_chat.id
    items = [line.strip() for line in update.message.text.splitlines() if line.strip()]
    if not items:
        await update.message.reply_text("No items found in your message.")
        return

    lock = user_locks.setdefault(chat_id, asyncio.Lock())
    async with lock:
        user_items[chat_id] = items

    await update.message.reply_text(f"Received {len(items)} items. Use /run to start processing.")


async def add_items(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add items to an existing list (append)."""
    chat_id = update.effective_chat.id
    items = [line.strip() for line in update.message.text.splitlines() if line.strip()]
    if not items:
        await update.message.reply_text("No items found to add.")
        return

    lock = user_locks.setdefault(chat_id, asyncio.Lock())
    async with lock:
        lst = user_items.setdefault(chat_id, [])
        lst.extend(items)
        count = len(lst)

    await update.message.reply_text(f"Added {len(items)} item(s). Total items now: {count}.")


async def list_items(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    items = user_items.get(chat_id, [])
    if not items:
        await update.message.reply_text("No items saved for this chat.")
        return
    text = "Current items:\n" + "\n".join(f"- {i}" for i in items)
    await update.message.reply_text(text)


async def clear_items(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    lock = user_locks.setdefault(chat_id, asyncio.Lock())
    async with lock:
        user_items.pop(chat_id, None)
    await update.message.reply_text("Cleared your items.")


async def run_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id

    existing_task = user_tasks.get(chat_id)
    if existing_task and not existing_task.done():
        await update.message.reply_text("Task is already running!")
        return

    items = user_items.get(chat_id)
    if not items:
        await update.message.reply_text("No items found. Send items first or use /add.")
        return

    # Start background task attached to the application loop
    task = context.application.create_task(process_items(chat_id, context))
    user_tasks[chat_id] = task
    await update.message.reply_text("Task started!")


async def stop_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    task = user_tasks.get(chat_id)
    if task and not task.done():
        task.cancel()
        try:
            # Await so we ensure cleanup in the task's except block runs
            await task
        except asyncio.CancelledError:
            # We expect this
            pass
        await update.message.reply_text("Task stopped!")
    else:
        await update.message.reply_text("No running task found.")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    task = user_tasks.get(chat_id)
    if task and not task.done():
        await update.message.reply_text("Task is running ✅")
    else:
        await update.message.reply_text("Task is not running ❌")


async def process_items(chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Background worker that processes items for a chat.
    This runs on the same event loop as the application. Long blocking work is delegated
    into threads via asyncio.to_thread.
    """
    logger.info("Starting processing for chat_id=%s", chat_id)
    lock = user_locks.setdefault(chat_id, asyncio.Lock())

    try:
        async with lock:
            items = list(user_items.get(chat_id, []))

        if not items:
            await context.bot.send_message(chat_id, text="No items to process.")
            return

        for idx, item in enumerate(items, start=1):
            # Periodically check if task was cancelled
            await asyncio.sleep(0)  # allow cancellation

            try:
                await context.bot.send_message(chat_id, text=f"Processing item {idx}/{len(items)}:\n{item}\n(While processing, commands will still work.)")
            except Conflict:
                logger.error("Conflict when sending processing message. Another instance may be running.")
                # Stop processing since bot instance conflict
                return

            # Run blocking price-check in a thread
            success = False
            last_exc = None
            for attempt in range(1, MAX_RETRIES + 2):
                try:
                    # If your get_all_store_price expects different args, update accordingly
                    result = await get_all_store_price(item)
                    # Optionally do something with result
                    await context.bot.send_message(chat_id, text=f"Result for '{item}': {result}")
                    success = True
                    break
                except Conflict:
                    logger.error("Conflict while sending result. Another instance or webhook active.")
                    return
                except Exception as e:
                    last_exc = e
                    logger.exception("Error while checking price for item=%s (attempt=%s)", item, attempt)
                    # brief backoff
                    await asyncio.sleep(1)

            if not success:
                try:
                    await context.bot.send_message(chat_id, text=f"Failed to process '{item}': {last_exc}")
                except Conflict:
                    logger.error("Conflict while sending failure message. Exiting.")
                    return

            # Delay between items
            await asyncio.sleep(DEFAULT_ITEM_DELAY)

        try:
            await context.bot.send_message(chat_id, text="All items processed ✅")
        except Conflict:
            logger.error("Conflict while sending completion message. Exiting.")

    except asyncio.CancelledError:
        logger.info("Processing cancelled for chat_id=%s", chat_id)
        # Notify the user that the task was cancelled
        try:
            await context.bot.send_message(chat_id, text="Task cancelled ❌")
        except Exception:
            logger.exception("Failed to notify chat about cancellation: %s", chat_id)
        raise
    except Exception:
        logger.exception("Unexpected error while processing items for chat_id=%s", chat_id)
        try:
            await context.bot.send_message(chat_id, text="An unexpected error occurred. Check logs.")
        except Exception:
            logger.exception("Failed to notify user of unexpected error for chat %s", chat_id)
    finally:
        # Clean up task reference
        t = user_tasks.get(chat_id)
        if t and t.done():
            user_tasks.pop(chat_id, None)
        logger.info("Processing finished for chat_id=%s", chat_id)


def build_app() -> ApplicationBuilder:
    token = get_bot_token()
    app = ApplicationBuilder().token(token).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("run", run_task))
    app.add_handler(CommandHandler("stop", stop_task))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("list", list_items))
    app.add_handler(CommandHandler("clear", clear_items))

    # Message handlers
    # If a user sends text that begins with /add, treat following lines as items to append.
    async def add_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # message text will include the '/add' prefix, so strip it
        text = update.message.text
        # remove the command part
        payload = text.partition(" ")[2] if " " in text else ""
        if not payload:
            await update.message.reply_text("Usage: /add <items> (one per line). You can also send a message with items directly to replace the list.)")
            return
        # reuse the same update but replace text for add_items
        original_text = update.message.text
        update.message.text = payload
        try:
            await add_items(update, context)
        finally:
            update.message.text = original_text

    app.add_handler(CommandHandler("add", add_wrapper))

    # A free-text message that is not a command replaces the items list
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_items))

    return app


def main() -> None:
    token = get_bot_token()

    # Attempt to remove any active webhook to avoid Conflict when polling
    try:
        info = requests.get(f"https://api.telegram.org/bot{token}/getWebhookInfo", timeout=10).json()
        url = info.get("result", {}).get("url")
        if url:
            logger.info("Deleting existing webhook: %s", url)
            requests.get(f"https://api.telegram.org/bot{token}/deleteWebhook", timeout=10)
    except Exception as e:
        logger.warning("Failed to check/delete webhook: %s", e)

    app = build_app()
    logger.info("Bot is starting... (press Ctrl+C to stop)")

    try:
        app.run_polling()
    except Conflict:
        logger.error("Conflict: another instance is running or a webhook exists. Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    main()
