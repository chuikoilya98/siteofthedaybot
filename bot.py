import requests
from bs4 import BeautifulSoup
import random
import datetime
import time
import logging
from dbconfig import Database
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext , MessageHandler, Filters

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
            if index != 10 :
               links.append(item['href'])
               index += 1
            else:
               break
            text = 'Я нашел такие сайты : \n'

            for i in links: 
               text += i
               text += ' \n'

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

def remove_job_if_exists(name: str, context: CallbackContext) -> bool:

   current_jobs = context.job_queue.get_jobs_by_name(name)
   if not current_jobs:
      return False
   for job in current_jobs:
      job.schedule_removal()
   return True

def start(update: Update, _: CallbackContext) -> None :

   info = update.message.from_user
   userId = info.id
   name = info.first_name

   userInfo = {
      'id' : userId,
      'name' : name
   }

   db = Database()
   kek = db.createNewUser(userInfo)

   update.message.reply_text(f'Привет, {name}! я бот, который умеет искать и предлагать необычные сайты. \n 1. Чтобы подписаться на ежедневную рассылку, напиши в чат команду  /siteoftheday "Час". Пример - /siteoftheday 14 \n 2. Чтобы получить ссылку на рандомный сайт, нажми /random \n 3. Чтобы найти сайты примеры, напиши поисковый запросы на английском ')

def getUsersCount(update: Update, context: CallbackContext) :
   adminId = '331392389'
   senderId = str(update.message.from_user.id)
   if adminId == senderId :
      db = Database()
      count = db.getAllUsers('count')
      message = f'Количество пользователей: {count}'
      context.bot.send_message(chat_id=adminId, text=message)


def findSites(update: Update, context: CallbackContext)-> None :
   adminId = '331392389'
   senderId = str(update.message.from_user.id)
   if adminId == senderId :
      db = Database()
      users = db.getAllUsers(key='id')
      for user in users :
         context.bot.send_message(chat_id=user, text=update.message.text)
      return 'success'
   else :
      search = update.message.text
      context.bot.send_message(chat_id=update.effective_chat.id, text='Секундочку, ищу примеры')
      aww = Inspiration()
      text = aww.getInspiration(search)
      context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def job(context: CallbackContext) -> None :
    
   job = context.job
   aww = Inspiration()
   text = aww.getSiteOfTheDay()
   context.bot.send_message(job.context, text = text)

def sendDailyMessage(update: Update, context: CallbackContext) -> None:
   chat_id = update.message.chat_id
   hour = int(context.args[0])
   timer = datetime.datetime.strptime(f'{hour-5}:00:00.000000', '%H:%M:%S.%f')
   job_removed = remove_job_if_exists(str(chat_id), context)
   context.job_queue.run_daily(callback = job,time = timer.time(), context= chat_id, name= str(chat_id))
   context.bot.send_message(chat_id=update.effective_chat.id, text=f'Теперь ты подписан на ежедневную рассылку! Она будет приходить каждый день в {hour}:00')

def timer(update: Update, _: CallbackContext) -> None :
    
   text = str(datetime.datetime.now())
   update.message.reply_text(text)

def randomSite(update: Update, context: CallbackContext) -> None :
   context.bot.send_message(chat_id=update.effective_chat.id, text='Подбираю рандомный сайт')
   aww = Inspiration()
   text = aww.getRandomSite()
   context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def main() -> None:

   updater = Updater("1755982457:AAGzuubLxQMJ36h8wjDsgTjvHZgUW6wiyRE")

   dispatcher = updater.dispatcher

   dispatcher.add_handler(CommandHandler("start", start))
   dispatcher.add_handler(CommandHandler("timer", timer))
   dispatcher.add_handler(CommandHandler("random", randomSite))
   dispatcher.add_handler(CommandHandler("siteoftheday", sendDailyMessage))
   dispatcher.add_handler(CommandHandler("count", getUsersCount))
   dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), findSites))
   

   updater.start_polling()

   updater.idle()

    
if __name__ == '__main__':
    
   current_date_time = datetime.datetime.now()
   current_time = current_date_time.time()
   main()
