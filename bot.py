# EN:
# Telegram interface for checking dollar and euro course to ruble
# and check COVID-19 situation in Russia and all over the world.
# 
# RU:
# Телеграмм бот для отслеживания курса доллара и евро к рублю
# и проверки ситуации коронавируса в России и по всему миру.
# 
# by grnbows

import config
import dataParser
import time
import telebot
import threading
import logging
import schedule
from pprint import pformat
from telebot import types
# from telebot import apihelper


# PROXY = 'socks5h://148.72.209.6:57437'
# apihelper.proxy = {'https': PROXY}

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


def getUsersList():
	global usersList
	file = open('users.txt')
	usersList = file.read().split(' ')
	usersList.pop()
	file.close()
	usersList = list(filter(lambda a: a != '', usersList))
	logging.info('Got the users list ' + str(usersList))
	return usersList


def getFollowersAmount():
	usersList = getUsersList()
	return len(usersList)


def addUserToUsersList(messageFromUserId):
	usersList = getUsersList()
	if str(messageFromUserId) in usersList:
		return False
		logging.info('Bad call, user ' + str(messageFromUserId) + ' in already in list')
	else:
		file = open('users.txt', 'a')
		file.write(str(messageFromUserId) + ' ')
		file.close()
		return True
		logging.info('New user' + str(messageFromUserId) + 'was added successfully')
		print(f'{messageFromUserId} was added to the list successfully\nCheck .log file for more info')


def delUserFromUsersList(messageFromUserId):
	usersList = getUsersList()
	if str(messageFromUserId) in usersList:
		usersList.remove(str(messageFromUserId))
		file = open('users.txt', 'w')
		stroke = ' '.join(usersList) + ' '
		file.write(stroke)
		file.close()
		stroke = ''
		return True
		logging.info('User' + str(messageFromUserId) + 'was deleted successfully')
		print(f'{messageFromUserId} was deleted from the list successfully\nCheck .log file for more info')
	else:
		return False
		logging.info('Bad call, user ' + str(messageFromUserId) + ' not fount in the list')


def sendEveryDayMessage():
	def sendNow(user):
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

		print(f'{serverTimeNow}: ' + 'everyday info message were send to ' + str(user) + ' successfully')
		logging.info(str(user) + ' took everyday info message now')

		bot.send_message(user, f'Время на сервере {serverTimeNow}.\n\
			\nВот такую информацию мне удалось собрать:\nКурс доллара: {dollarNow}\nКурс евро: {euroNow}\n\
			\nCOVID-19 в России на {serverDateNow}\nВсего случаев: {ruAll}\nВыздоровело: {ruRecovered}\nСмертей: {ruDies}\n\
			\nCOVID-19 в мире:\nВсего случаев: {worldAll}\nВыздоровело: {worldRecovered}\nСмертей: {worldDies}\n\
			\nСпасибо, что подписались на ежедневную рассылку❤️')
	

	def sendingOrg():
		usersList = getUsersList()

		for i in range(len(usersList)):
			if usersList[i] != '' and usersList[i] != None:
				sendNow(usersList[i])

		serverTimeNow = getServerData()['time']
		print('\n\n' + '#' * 30 + '\nNewsletter is over\n' + '#' * 30 + '\n\n')
		logging.info('\n\n' + '#' * 30 + '\nNewsletter infos over\n' + '#' * 30 + '\n\n')


	schedule.every().day.at("12:35").do(sendingOrg)

	while True:
		schedule.run_pending()
		time.sleep(1)

# data variables
dataDict = getNewData()
usersList = []


# bot body
bot = telebot.TeleBot(config.TOKEN)

print('\n' * 30  + '#' * 30 + '\nNow it\'s started successfully.\nINFO: Server Time:' + getServerData()['time'] + '\nData Dictionary Parsed successfully.\n' + '#' * 30 + '\n\nData for now:')
print(pformat(dataDict))
print('\n\n')
logging.info('\n\n\n' + '#' * 50 +'\nNow it\'s started successfully.\n' + '#' * 50)


@bot.message_handler(commands=['start', 'старт', 'начать'])
def sendWelcomeMessage(message):
	if message.chat.type == 'private':
		serverTimeNow = getServerData()['time']

		print(f'{serverTimeNow}: ' + str(message.from_user.id) + ' used /start command now')
		logging.info(str(message.from_user.id) + ' used /start command now')

		bot.send_message(message.chat.id, 'Добро пожаловать, {0.first_name}.\nЯ - <b>{1.first_name}</b> - бот для учета важной информации на день.\n\
			\nНа сегодня актуально:\n•Курс доллара и евро\n•Ситуация COVID-19 в России и мире\n\
			\nНапиши команду <b><i>/info</i></b>, чтобы узнать актуальную информацию на нынешний момент.\n\
			\n<b><i>/help</i></b> - для полного списка команд.\
			'.format(message.from_user, bot.get_me()), parse_mode='html')
	else:
		bot.send_message(message.chat.id, 'Бот не поддерживает работу в групповых чатах.\n\
			\nФункция дорабатывается, разработчик у бота один. Прошу прощения за неудобства, скоро пофикшу,\nДенис')


@bot.message_handler(commands=['help', 'commands', 'помощь'])
def sendHelpList(message):
	if message.chat.type == 'private':
		serverTimeNow = getServerData()['time']

		print(f'{serverTimeNow}: ' + str(message.from_user.id) + ' used /help command now')
		logging.info(str(message.from_user.id) + ' used /help command now')

		bot.send_message(message.chat.id, 'Доступные команды:\n\
			\n<b><i>/info</i></b> - получить сводку на нынешний момет\n\
			\n<b><i>/sub</i></b> - подписаться на ежедневную автоматическую рассылку сводки. Она будет приходить в 8:00 (UTC +3)\n\
			\n<b><i>/unfollow</i></b> - отписаться от ежедневной рассылки сводки\n\
			\n<b><i>/report</i></b> - сообщить об ошибке в работе бота\n\
			\n<b><i>/author</i></b> - посмотреть информацию о разработчике\n\
			'.format(message.from_user, bot.get_me()), parse_mode='html')
	else:
		bot.send_message(message.chat.id, 'Бот не поддерживает работу в групповых чатах.\n\
			\nФункция дорабатывается, разработчик у бота один. Прошу прощения за неудобства, скоро пофикшу,\nДенис')


@bot.message_handler(commands=['записаться', 'регулярно', 'sub', 'subscribe'])
def subThePerson(message):
	if message.chat.type == 'private':
		serverTimeNow = getServerData()['time']
		
		print(f'{serverTimeNow}: ' + str(message.from_user.id) + ' used /sub command now')
		logging.info(str(message.from_user.id) + ' used /sub command now')

		feedback = addUserToUsersList(message.chat.id)

		if feedback == True:
			bot.send_message(message.chat.id, 'Подписка на ежедневную рассылку успешно оформлена.\n\
				\n<b><i>/unfollow</i></b> - отписаться.\n\
				'.format(message.from_user, bot.get_me()), parse_mode='html')

			logging.info(str(message.chat.id) + 'subscribed successfully') 
		else:
			bot.send_message(message.chat.id, 'Вы уже подписаны на рассылку, повторная подписка невозможна.\n\
				\nБот ошибается? /report\n')		
	else:
		bot.send_message(message.chat.id, 'Бот не поддерживает работу в групповых чатах.\n\
			\nФункция дорабатывается, разработчик у бота один. Прошу прощения за неудобства, скоро пофикшу,\nДенис')


@bot.message_handler(commands=['отписаться', 'unfollow', 'unf', 'unsub'])
def unfollowThePerson(message):
	if message.chat.type == 'private':
		serverTimeNow = getServerData()['time']
		
		print(f'{serverTimeNow}: ' + str(message.from_user.id) + ' used /unfollow command now')
		
		logging.info(str(message.from_user.id) + ' used /unfollow command now')
		feedback = delUserFromUsersList(message.chat.id)

		if feedback == True:
			bot.send_message(message.chat.id, 'Вы успешно отписались от рассылки.\n\
				\n<b><i>/sub</i></b> - подписаться вновь.\n<b><i>/help</i></b> - список команд.\
				'.format(message.from_user, bot.get_me()), parse_mode='html')

			logging.info(str(message.chat.id) + 'unfollowed successfully') 
		else:
			bot.send_message(message.chat.id, 'Нужно быть подписанным, чтобы была возможность отписаться.\n\
				\n/sub - подписаться.\n\
				\nБот ошибается? /report\n')	
		
	else:
		bot.send_message(message.chat.id, 'Бот не поддерживает работу в групповых чатах.\n\
			\nФункция дорабатывается, разработчик у бота один. Прошу прощения за неудобства, скоро пофикшу,\nДенис')


@bot.message_handler(commands=['report', 'ошибка', 'баг'])
def sendReport(message):
	if message.chat.type == 'private':
		serverTimeNow = getServerData()['time']

		bot.send_message(message.chat.id, 'Сообщить о работе бота можно @grnbows в личных сообщениях Telegram по следующей форме:\n\
			\n1. Примерное время возникновения ошибки.\n2. Скрин места переписки, где наглядно видна ошибка.\n3. Краткое описание проблемы своими словами.\n4. Скрин/переслать сообщение, что придёт следующим.\n\
			\nСпасибо за помощь в разработке бота. Ваши отзывы очень помогают разобраться в проблеме.\n')
		bot.send_message(message.chat.id, 'message.chat.id - ' + str(message.chat.id) + '\nmessage.from_user.id - ' + str(message.from_user.id) + '\nmessage.chat.type - ' + str(message.chat.type))
		
		print(f'{serverTimeNow}: ' + str(message.from_user.id) + ' used /report command now')
		logging.info(str(message.from_user.id) + ' used /report command now')
	else:
		bot.send_message(message.chat.id, 'Бот не поддерживает работу в групповых чатах.\n\
			\nФункция дорабатывается, разработчик у бота один. Прошу прощения за неудобства, скоро пофикшу,\nДенис')


@bot.message_handler(commands=['автор', 'grnbows', 'разработчик', 'программист', 'author'])
def sendAuthorInfo(message):
	serverTimeNow = getServerData()['time']

	amountOfUsers = getFollowersAmount()

	markup = types.InlineKeyboardMarkup()
	buttonVk = types.InlineKeyboardButton(text='Вконтакте', url='https://vk.com/grnbows')
	buttonInsta = types.InlineKeyboardButton(text='Instagram', url='https://www.instagram.com/grnbows/')
	markup.add(buttonVk, buttonInsta)

	print(f'{serverTimeNow}: ' + str(message.from_user.id) + ' used /author command now')
	logging.info(str(message.from_user.id) + ' used /author command now')

	bot.send_message(message.chat.id, f'Разработчик бота: @grnbows\n\
		\nСо мной можно связаться в Telegram или в других социальных сетях, например ВКонтакте или Instagram. Везде тег такой же - @grnbows.\n\
		\nСпасибо за проявленный интерес к этому проекту, Вы позволяете мне развиваться в программировании дальше.\n\
		\n/donate - для моих реквизитов.\n\
		\nПодписчиков в системе: {amountOfUsers}\nПоследняя актуальная версия бота: {config.__BOT_VESION}', reply_markup = markup)


@bot.message_handler(commands=['донат', 'помочь', 'donate', 'реквизиты'])
def sendRequisites(message):
	serverTimeNow = getServerData()['time']

	print(f'{serverTimeNow}: ' + str(message.from_user.id) + ' used /donate command now')
	logging.info(str(message.from_user.id) + ' used /donate command now')

	bot.send_message(message.chat.id, 'Список моих реквизитов недоступен, бот в разработке.\nСпасибо.\
		'.format(message.from_user, bot.get_me()), parse_mode='html')
	bot.send_sticker(message.chat.id, open('images/donate.tgs', 'rb'))


@bot.message_handler(commands=['info', 'инфо', 'информация'])
def sendInfoNow(message):
	if message.chat.type == 'private':
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


reloadDataThread = threading.Thread(target=reloadData, name='reloadDataThread')
sendEveryDayMessageThread = threading.Thread(target=sendEveryDayMessage, name='sendEveryDayMessageThread')
sendEveryDayMessageThread.start()
reloadDataThread.start()
bot.polling(none_stop=True, interval=0)
