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
import schedule
import logging


logging.basicConfig(filename='botbody.log',
					level=logging.INFO,
					format='%(asctime)s///%(levelname)s///%(funcName)s/// - %(message)s')


def getServerData():
	serverTime = str(int(time.strftime('%H')) - 1) + ':' + time.strftime('%M:%S (UTC +3)')
	serverDate = time.strftime('%d:%m:20%y')
	logging.info('Server Data get successfully')
	return {'time': serverTime,
			'date': serverDate
			}


def getNewData():
	dollarNow = dataParser.checkDollarValue() # get currency info
	euroNow = dataParser.checkEuroValue()

	ruCorona = dataParser.checkCoronaRussia() # get dict vith coronavirus in russia info

	ruAll = ruCorona['all']
	ruRecovered = ruCorona['recovered']
	ruDies = ruCorona['dies']
	dict = {'dollar': dollarNow, 
			'euro': euroNow, 
			'coronaRus': {
				'all': ruCorona['all'], 
				'recovered': ruCorona['recovered'],
				'dies': ruCorona['dies'] },
			'coronaWorld': {
				'all': None, 
				'recovered': None,
				'dies': None }
			}
	logging.info('New Parse Data was taken' + str(dict))
	return dict

# schedule.every(15).minutes.do(getNewData)
# bot body
# start command
bot = telebot.TeleBot(config.TOKEN)

print('Now it\'s started successfully.')
logging.info('\n\nNow it\'s started successfully.\n\n')


@bot.message_handler(commands=['start', 'старт', 'начать'])
def sendWelcomeMessage(message):
	bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}.\nЯ - <b>{1.first_name}</b> - бот для учета важной,\
	 по мнению автора, информации на день.\n\nКаждый день в 8:00 по МСК (UTC +3) я буду отправлять тебе курс доллара и евро\
	 по отношению к рублю, а также новую информацию о COVID-19 в России.\n\nЕсли хочешь узнать обновлённую информацию, то\
	 просто напиши команду <b><i>/info</i></b> и я достану самую актуальную на запрашиваемый момент информацию.\
	 '.format(message.from_user, bot.get_me()), parse_mode='html')


# info command
@bot.message_handler(commands=['info', 'инфо', 'информация'])
def sendInfoNow(message):
	serverTimeNow = getServerData()['time']
	serverDateNow = getServerData()['date']

	dollarNow = getNewData()['dollar']
	euroNow = getNewData()['euro']

	ruAll = getNewData()['coronaRus']['all']
	ruRecovered = getNewData()['coronaRus']['recovered']
	ruDies = getNewData()['coronaRus']['dies']

	bot.send_message(message.chat.id, f'Время на сервере {serverTimeNow}.\n\
		\nВот такую информацию мне удалось собрать:\nКурс доллара: {dollarNow}\nКурс евро: {euroNow}\n\
		\nCOVID-19 в России на {serverDateNow}\nВсего случаев: {ruAll}\nВыздоровело: {ruRecovered}\nСмертей: {ruDies}')


bot.polling(none_stop=True, interval=0)
# schedule.every().day.at("10:30").do(job)