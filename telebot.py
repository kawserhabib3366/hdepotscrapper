from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import asyncio

from check_price import get_all_store_price

# Dictionary to store tasks per chat
user_tasks = {}
user_items = {}

# Start command: ask for items
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send me the list of items (one per line) and then press /run to start the task."
    )

# Receive list of items from user
async def receive_items(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    items = update.message.text.splitlines()
    user_items[chat_id] = [item.strip() for item in items if item.strip()]
    await update.message.reply_text(
        f"Received {len(user_items[chat_id])} items. Use /run to start the task."
    )

# Run task
async def run_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id in user_tasks and not user_tasks[chat_id].done():
        await update.message.reply_text("Task is already running!")
        return

    if chat_id not in user_items or not user_items[chat_id]:
        await update.message.reply_text("No items found. Send items first.")
        return

    # Start background task
    task = asyncio.create_task(process_items(chat_id, context))
    user_tasks[chat_id] = task
    await update.message.reply_text("Task started!")

# Stop task
async def stop_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    task = user_tasks.get(chat_id)
    if task and not task.done():
        task.cancel()
        await update.message.reply_text("Task stopped!")
    else:
        await update.message.reply_text("No running task found.")

# Check status
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    task = user_tasks.get(chat_id)
    if task and not task.done():
        await update.message.reply_text("Task is running ✅")
    else:
        await update.message.reply_text("Task is not running ❌")

# Background processing
async def process_items(chat_id, context):
    try:
        for item in user_items.get(chat_id, []):
            # Simulate processing (replace with your logic)
            print(f"Processing item {item} for chat {chat_id}")
            await context.bot.send_message(chat_id, text=f"Processing item: {item} /n while processing no command should work")


            get_all_store_price(itemId=item)


            await asyncio.sleep(2)  # delay between items


        await context.bot.send_message(chat_id, text="All items processed ✅")
    except asyncio.CancelledError:
        await context.bot.send_message(chat_id, text="Task cancelled ❌")

if __name__ == "__main__":
    app = ApplicationBuilder().token("7209908346:AAGUKR0abafZ8ddkAUTclg8qpysEB9-h0dk").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("run", run_task))
    app.add_handler(CommandHandler("stop", stop_task))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_items))

    print("Bot is running...")
    app.run_polling()
