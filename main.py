import requests
from bs4 import BeautifulSoup
import re
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext

import os


PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

TOKEN = "5314258275:AAGhajt1ao0fS-LXaI0tzOmCOwLR8Ldk5tw"


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    userneng = update.message.from_user.username
    message = update.message.text + " " + userneng
    update.message.reply_text(message)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")


def check(update: Update, context: CallbackContext) -> None:
    #baseURL = "https://api.telegram.org/bot1571549234:AAErHX8AgGiKGTxTHZsT91zprREJfiIcNEs/sendMessage"
 #   chatID = "-1001410978577"
    # message=str(context.args)
    message = update.message.text
    # message=message.lstrip("/relay ")
    message = message.split(" ", 2)
    query = message[1]

    #query=input("Mau cari apa hari ni:\n")
    search_url= f"https://bco.com.my/?subcats=Y&pcode_from_q=Y&pshort=Y&pfull=Y&pname=Y&pkeywords=Y&search_performed=Y&pshort=N&pfull=N&pname=Y&pkeywords=Y&pcode=Y&match=all&q={query}&dispatch=products.search&security_hash=2b1c210c28b6e00fa5f0927825a578d4"
    response=requests.get(search_url)
    result=response.text
    soup=BeautifulSoup(result,"html.parser")
    alltitle=soup.find_all(name="a" , class_="product-title")
   # replyText=" "
    if len(alltitle)==0:
        update.message.reply_text("Not Found")

    else:
        result_title=[]
        result_url=[]
        outPut=[]

        for rob in alltitle:
            result_title.append(rob.getText())
            result_url.append(rob.get("href"))


        for deep in result_url:
            responsedeep = requests.get(deep)
            resultdeep = responsedeep.text
            soupdeep = BeautifulSoup(resultdeep, "html.parser")
            titleraw=soupdeep.find(name="h1", class_="ty-product-block-title")
            stockraw = soupdeep.find(name="div" , id=re.compile("^product_amount_update_"))
            titleText=titleraw.getText()
            stockText=stockraw.getText()
            stocklastText=stockText.split(":",2)
            stockText=stocklastText[1].strip()
            print(titleText)
            print (stockText)
            outPut.append(f"{titleText} \n Stock: {stockText} \n Url:{deep}")
            replyText=f"{titleText}  {stockText}"
            update.message.reply_text(replyText)
  #update.message.reply_text(botreplyText, reply_markup=reply_markup)

 #   with open("movie.txt",'w') as outFile:
  #      for out in outPut:
  #      outFile.write(f"{out}\n")

#------#

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("check", check))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("echo", echo))

    # on noncommand i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('bcocheck.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
