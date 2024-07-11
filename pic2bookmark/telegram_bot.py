import logging
import os
import re
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)

from easy_bookmark.notion_uploader import NotionUploader
from extraction.image_extraction import main
from telegram.constants import ParseMode

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def help_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("""**Title**: Financials: Income Statement Projection (2015-2019)

**Summary**: This document provides a detailed projection of the income statement for the years 2015 to 2019, highlighting revenue, expenses, gross profit, and net profit.

**Key Points**:
- Displayed income statement projection from 2015 to 2019.
- Key metrics included: Revenue, Cost of Goods Sold, Gross Profit, Expenses, Earning Before Taxes, and Net Profit.
- Notable growth in revenue and net profit over the five-year period.""".replace(".", "\.").replace("(", "\(").replace(")", "\)").replace("-", "\-"), parse_mode=ParseMode.MARKDOWN_V2)


async def extract_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    llm_client = OpenAI()
    database_id="69063e81e25b479db72122690a9e2f54"
    uploader = NotionUploader(token=os.environ["NOTION_TOKEN"])
    path_to_save = "images/img.jpg"

    last_pic = update.message.photo[-1]
    file = await context.bot.get_file(last_pic)
    await file.download_to_drive(path_to_save)
    await update.message.reply_text("Processing file!!")

    llm_output: str = await main(llm_client=llm_client, image_path=path_to_save)
#    llm_output: str = """**Title**: Financials: Income Statement Projection (2015-2019)
#
#**Summary**: This document provides a detailed projection of the income statement for the years 2015 to 2019, highlighting revenue, expenses, gross profit, and net profit.
#
#**Key Points**:
#- Displayed income statement projection from 2015 to 2019.
#- Key metrics included: Revenue, Cost of Goods Sold, Gross Profit, Expenses, Earning Before Taxes, and Net Profit.
#- Notable growth in revenue and net profit over the five-year period.""".replace(".", "\.").replace("(", "\(").replace(")", "\)").replace("-", "\-")
    pattern = r'\*\*Title\*\*: (.*?)\n'
    match = re.search(pattern, llm_output)

    if match:
        title = match.group(0).replace("\\","").replace("*","").lstrip("Title: ").rstrip("\n")

    response = uploader.create_notion_page(database_id, title=title, content=llm_output)
    await update.message.reply_text(f"https://www.notion.so/{response.json()["id"].replace("-","")}")
    await update.message.reply_text(llm_output)


if __name__ == "__main__":
    application = (
        ApplicationBuilder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    )

    start_handler = CommandHandler("start", start)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("extract", extract_command))
    application.add_handler(MessageHandler(filters.PHOTO, extract_command))

    application.add_handler(start_handler)

    application.run_polling(timeout=200000, read_timeout=200000)
