import requests
from bs4 import BeautifulSoup
import random
import sqlite3
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

#TODO: Перенести в разные файлы
class Database() :
    pass

class Inspiration() :

    mainUrl = 'https://www.awwwards.com/'
    searchUrl = 'https://www.awwwards.com/inspiration/search?text='
    randomUrl = 'https://www.awwwards.com/websites/nominees/'
    searchParam = '&type=submission'
    headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'    
        }

    def getSiteOfTheDay(self) -> str :

        html = requests.get(self.mainUrl, headers=self.headers)
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'lxml')

        link = soup.find('div', class_='box-bl gap')
        siteOfTheDay = link.find('a')['href']

        text = f"Интересный сайт на сегодня - {siteOfTheDay}"

        return text

    def getInspiration(self,request:str) -> str :

        url = self.searchUrl + request + self.searchParam
        html = requests.get(url, headers=self.headers)
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'lxml')

        try :
            items = soup.find_all('a', class_='button x-small border-black circle js-visit-item')
            links =[]
            index = 0
            
            for item in items :
                while index < 10 or index < len(items) :
                    links.append(item['href'])
                    index += 1

            text = 'Я нашел такие сайты : \n'

            for i in links: 
                text += i

            #make db action
            return text                

        except AttributeError:

            text = 'К сожалению, я ничего не нашел. Попробуй другой поисковый запрос'
            #make db action
            return text

    def getRandomSite(self) -> str :
        url = self.randomUrl
        html = requests.get(url, headers=self.headers)
        html.encoding = 'utf-8'
        soup = BeautifulSoup(html.text, 'lxml')

        sites = soup.find_all('a', class_='button x-small border-black circle js-visit-item')
        index = random.randint(0, len(sites))

        site = sites[index]['href']

        text = f'Рандомный сайт - {site}'

        return text

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, _: CallbackContext) -> None :
    #make db write for info about User
    update.message.reply_text('Привет, я бот, который умеет искать и предлагать необычные сайты. Чтобы подписаться на ежедневную рассылку, нажми /siteoftheday')

def job(context: CallbackContext) -> None :
    
    job = context.job
    aww = Inspiration()
    text = aww.getSiteOfTheDay()
    context.bot.send_message(job.context, text = text)

def sendDailyMessage(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    context.job_queue.run_daily(callback = job,time = None, context= chat_id, name= str(chat_id))

def main() -> None:

    updater = Updater("1755982457:AAGzuubLxQMJ36h8wjDsgTjvHZgUW6wiyRE")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("siteoftheday", sendDailyMessage))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()