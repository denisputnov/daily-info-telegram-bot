# EN:
# Telegram interface for checking dollar and euro course to ruble
# and check COVID-19 situation in Russia and all over the world. (last function in work)
# 
# RU:
# Телеграмм бот для отслеживания курса доллара и евро к рублю
# и проверки ситуации коронавируса в России и по всему миру. (Последняя функция в разработке)
# 
# by grnbows

import config
import dataParser
import time
import telebot
import threading
import logging
from pprint import pformat

logging.basicConfig(filename='botbody.log',
					level=logging.INFO,
					format='%(asctime)s///%(levelname)s///%(funcName)s/// - %(message)s')


def getServerData():
	serverTime = str(int(time.strftime('%H')) - 1) + ':' + time.strftime('%M:%S (UTC +3)')
	serverDate = time.strftime('%d.%m.20%y')
	logging.info('Server Data get successfully')
	return {'time': serverTime,
			'date': serverDate
			}


def getNewData():
	dollarNow = dataParser.checkDollarValue() # get currency info
	euroNow = dataParser.checkEuroValue()

	ruCorona = dataParser.checkCoronaRussia() # get dict vith coronavirus 
	worldCorona = dataParser.checkCoronaWorld()

	global dataDict
	dataDict = {'dollar': dollarNow, 
			'euro': euroNow, 
			'coronaRus': {
				'all': ruCorona['all'], 
				'recovered': ruCorona['recovered'],
				'dies': ruCorona['dies'] },
			'coronaWorld': {
				'all': worldCorona['all'], 
				'recovered': worldCorona['recovered'],
				'dies': worldCorona['dies'] }
			}
	return dataDict


def reloadData():
	global dataDict
	while True:
		time.sleep(config.PARSE_DELAY)
		serverTimeNow = getServerData()['time']
		getNewData()
		print(f'\n{serverTimeNow} - New data was taken successfully:\n' )
		print(pformat(dataDict))
		print('\n\n')
		logging.info('New data was taker successfully  - ' + str(dataDict))


dataDict = getNewData()
# bot body
# start command
bot = telebot.TeleBot(config.TOKEN)

print('\n' * 30  + '#' * 30 + '\nNow it\'s started successfully.\nINFO: Server Time:' + getServerData()['time'] + '\nData Dictionary Parsed successfully.\n' + '#' * 30 + '\n\nData for now:')
print(pformat(dataDict))
print('\n\n')
logging.info('\n\n\n' + '#' * 50 +'\nNow it\'s started successfully.\n' + '#' * 50)


@bot.message_handler(commands=['start', 'старт', 'начать'])
def sendWelcomeMessage(message):
	serverTimeNow = getServerData()['time']

	print(f'{serverTimeNow}: ' + str(message.from_user.id) + ' used /start command now')
	logging.info(str(message.from_user.id) + ' used /start command now')

	bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}.\nЯ - <b>{1.first_name}</b> - бот для учета важной информации на день.\n\
		\nНа сегодня актуально:\n•Курс доллара и евро\n•Ситуация COVID-19 в России и мире\n\
		\nНапиши команду <b><i>/info</i></b>, чтобы узнать актуальную информацию на нынешний момент.\
	 	'.format(message.from_user, bot.get_me()), parse_mode='html')



@bot.message_handler(command=['записаться', 'регулярно', 'sub', 'subscribe'])
def subThePerson(message):
	pass


# add command that'l show author


# info command
@bot.message_handler(commands=['info', 'инфо', 'информация'])
def sendInfoNow(message):
	if message.chat.type == "private":
		serverTimeNow = getServerData()['time']
		serverDateNow = getServerData()['date']

		dollarNow = dataDict['dollar']
		euroNow = dataDict['euro']

		ruAll = dataDict['coronaRus']['all']
		ruRecovered = dataDict['coronaRus']['recovered']
		ruDies = dataDict['coronaRus']['dies']

		worldAll = dataDict['coronaWorld']['all']
		worldRecovered = dataDict['coronaWorld']['recovered']
		worldDies = dataDict['coronaWorld']['dies']

		print(f'{serverTimeNow}: ' + str(message.from_user.id) + ' used /info command now')
		logging.info(str(message.from_user.id) + ' used /info command now')

		bot.send_message(message.chat.id, f'Время на сервере {serverTimeNow}.\n\
			\nВот такую информацию мне удалось собрать:\nКурс доллара: {dollarNow}\nКурс евро: {euroNow}\n\
			\nCOVID-19 в России на {serverDateNow}\nВсего случаев: {ruAll}\nВыздоровело: {ruRecovered}\nСмертей: {ruDies}\n\
			\nCOVID-19 в мире:\nВсего случаев: {worldAll}\nВыздоровело: {worldRecovered}\nСмертей: {worldDies}')
	else:
		bot.send_message(message.chat.id, 'Бот не поддерживает работу в групповых чатах.\n\
			\nФункция дорабатывается, разработчик у бота один. Прошу прощения за неудобства, скоро пофикшу,\nДенис')


threadManager = threading.Thread(target=reloadData, name='ReloadDataThread')
threadManager.start()
bot.polling(none_stop=True, interval=0)

# schedule.every().day.at("10:30").do(job)