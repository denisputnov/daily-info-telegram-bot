# EN:
# Telegram interface for cheching dollar and euro course to ruble
# and check COVID-19 situation in Russia and all over the world. (last function in work)
# 
# RU:
# Телеграмм бот для отслеживания курса доллара и евро к рублю
# и проверки ситуации коронавируса в России и по всему миру. (Последняя функция в разработке)
# 
# by grnbows


import requests
from bs4 import BeautifulSoup as bs
import time
import telebot

# telebot settings
TOKEN = '1147139388:AAFVG4IWQx6648uj0PoKY7aJfkz85n0_-r4' # bot token from @BotFather
ADMIN_ID = '587125336' # admin id to stop the bot

# parce links
DOLLAR_RUB = 'https://www.google.com/search?sxsrf=ALeKk019mDZuHXl_kJn236jQiujlWmdMfA%3A1585593896838&ei=KD6CXpPVMqummwXF4pLIBg&q=курс+доллара+к+рублю&oq=курс+доллара+к+рублю&gs_lcp=CgZwc3ktYWIQAzIKCAAQgwEQRhCCAjIFCAAQgwEyBQgAEIMBMgIIADICCAAyAggAMgUIABCDATICCAAyAggAMgUIABCDAToECAAQRzoECCMQJzoJCCMQJxBGEIICOgQIABBDOgcIABCDARBDOgoIABCDARAUEIcCOgQIABAKULrPBVj78QVglvQFaAJwAXgAgAGIAogBtiCSAQYwLjE0LjiYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwiTierH7cLoAhUr06YKHUWxBGkQ4dUDCAs&uact=5'
EURO_RUB = 'https://www.google.com/search?sxsrf=ALeKk01nxxm7rMTNB_K1L5zriJ4mUVu0fg%3A1585594081312&ei=4T6CXunREsvAmwXG7quQCw&q=курс+евро+к+рублю&oq=курс+евро+к+рублю&gs_lcp=CgZwc3ktYWIQAzIKCAAQgwEQFBCHAjIKCAAQgwEQFBCHAjICCAAyAggAMgUIABCDATIFCAAQgwEyAggAMgIIADICCAAyAggAOgQIABBHOgQIABANOggIABAIEA0QHjoGCAAQCBAeOgYIABAHEB46CQgjECcQRhCCAjoECCMQJzoPCAAQgwEQFBCHAhBGEIICULAkWKVTYNJUaABwAngBgAGEAogBiB6SAQYwLjEyLjiYAQCgAQGqAQdnd3Mtd2l6&sclient=psy-ab&ved=0ahUKEwipxuWf7sLoAhVL4KYKHUb3CrIQ4dUDCAs&uact=5'
CORONA_RUSSIA = 'https://yandex.ru/search/?text=количество%20заражённых%20коронавирусом&clid=2270455&banerid=0500000134%3A5dd0188f372d7c00241a7bf2&win=411&lr=11144&redircnt=1585586377.1'
CORONA_WORLD = 'https://coronavirus-monitor.ru/statistika/'

# parsing client settings, user status
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}


# parsing functions block
def checkDollarValue():
	dollarFullPage = requests.get(DOLLAR_RUB, headers=headers)
	dollarSoup = bs(dollarFullPage.content, 'html.parser')
	dollarConvert = dollarSoup.findAll('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})
	return dollarConvert[0].text


def checkEuroValue():
	euroFullPage = requests.get(EURO_RUB, headers=headers)
	euroSoup = bs(euroFullPage.content, 'html.parser')
	euroConvert = euroSoup.findAll('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})
	return euroConvert[0].text


def checkCoronaRussia():
	coronaRusiiaFullPage = requests.get(CORONA_RUSSIA, headers=headers)
	coronaRussiaSoup = bs(coronaRusiiaFullPage.content, 'html.parser')
	coronaRussiaConvert = coronaRussiaSoup.findAll('b')
	return {'all': coronaRussiaConvert[0].text, 'recovered': coronaRussiaConvert[1].text, 'dies': coronaRussiaConvert[2].text}


def checkCoronaWorld():
	coronaWorldFullPage = requests.get(CORONA_WORLD, headers=headers)
	coronaWorldSoup = bs(coronaWorldFullPage.content, 'html.parser')
	coronaWorldConvert = coronaWorldSoup.findAll('div', {'class': 'value', 'class': 'js-confirmed-value'})
	return coronaWorldConvert


# print(checkDollarValue())
# print(checkEuroValue())



# bot body
bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start', 'старт', 'начать'])
def sendWelcomeMessage(message):
	bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}.\nЯ - <b>{1.first_name}</b> - бот для учета важной,\
	 по мнению автора, информации на день.\n\nКаждый день в 8:00 по МСК (UTC +3) я буду отправлять тебе курс доллара и евро \
	 по отношению к рублю, а также новую информацию о COVID-19 в России.\n\nЕсли хочешь узнать обновлённую информацию, то\
	 просто напиши команду <b><i>/info</i></b> и я достану самую актуальную на запрашиваемый момент информацию.\
	 '.format(message.from_user, bot.get_me()), parse_mode='html')

@bot.message_handler(commands=['info', 'инфо', 'информация'])
def sendInfoNow(message):
	print(str(message.from_user.id) + ' used /info')
	dollarNow = checkDollarValue()
	print('dollarNow good')
	euroNow = checkEuroValue()
	print('euroNow good')
	ruCorona = checkCoronaRussia()
	ruAll = ruCorona['all']
	print('ruAll good')
	ruRecovered = ruCorona['recovered']
	print('ruRecovered good')
	ruDies = ruCorona['dies']
	print('ruDies ok')
	serverTime = str(int(time.strftime('%H')) - 1) + ':' + time.strftime('%M:%S (UTC +3)')
	serverDate = time.strftime('%d:%m:20%y')
	bot.send_message(message.chat.id, f'Время на сервере {serverTime}.\n\
		\nВот такую информацию мне удалось собрать:\nКурс доллара: {dollarNow}\nКурс евро: {euroNow}\n\
		\nCOVID-19 в России на {serverDate}\nВсего случаев: {ruAll}\nВыздоровело: {ruRecovered}\nСмертей: {ruDies}')

bot.polling(none_stop=True, interval=0)


