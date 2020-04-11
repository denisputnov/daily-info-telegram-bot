"""
EN: 
Telegram interface for checking dollar and euro course to ruble
and check COVID-19 situation in Russia and all over the world.

RU:
Телеграмм бот для отслеживания курса доллара и евро к рублю
и проверки ситуации коронавируса в России и по всему миру.

Use    python bot.py    command to start

Params: None

Copyright © 2020 Denis Putnov. All rights reserved.
"""

import config
import dataParser
import time
import telebot
import threading
import logging
import schedule
from pprint import pformat
from telebot import types


logging.basicConfig(filename='botbody.log',
					level=logging.INFO,
					format='%(asctime)s///%(levelname)s///%(funcName)s/// - %(message)s')


def get_server_data():
	"""
	get_server_data(params=None)

	return dictionary {'time': serverTime,'date': serverDate}
	"""
	serverTime = str((int(time.strftime('%H')) - 1) % 24) + ':' + time.strftime('%M:%S (UTC +3)')
	serverDate = time.strftime('%d.%m.20%y')
	logging.info('Server Data get successfully')
	return {'time': serverTime,
			'date': serverDate
			}


def get_new_data():
	"""
	get_new_data(params=None)
	
	Use    dataParser.py    and make dictionary with data

	return dictionary with keys:
		dollar, euro, coronaRus(all, recovered, dies), coronaWorld(all, recovered, dies)
	"""
	dollarNow = dataParser.check_dollar_value()
	euroNow = dataParser.check_euro_value()

	ruCorona = dataParser.check_corona_russia()
	worldCorona = dataParser.check_corona_world()

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


def reload_data():
	"""
	reload_data(params=None)

	Use    get_new_data(params=None)    function to reload local data.

	return dictionary with reloaded info 
	"""
	global dataDict
	while True:
		time.sleep(config.PARSE_DELAY)
		serverTimeNow = get_server_data()['time']
		get_new_data()
		print(f'\n{serverTimeNow} - New data was taken successfully:\n' )
		print(pformat(dataDict))
		print('\n\n')
		logging.info('New data was taker successfully  - ' + str(dataDict))


def get_users_list():
	"""
	get_users_list(params=None)

	return all user identificators from    users.txt    as list.
	"""
	global usersList
	file = open('users.txt')
	usersList = file.read().split(' ')
	usersList.pop()
	file.close()
	usersList = list(filter(lambda a: a != '', usersList))
	logging.info('Got the users list ' + str(usersList))
	return usersList


def get_followers_amount():
	"""
	get_followers_amount(params=None)
    
	return len(get_users_list(params=None))
	"""
	usersList = get_users_list()
	return len(usersList)


def add_user_to_users_list(messageFromUserId):
	"""
	add_user_to_users_list(messageFromUserId)
	
	Add user to    users.txt
	messageFromUserId: id of user, that used /sub command.
	
	Use    get_users_list(params=None)    function to get a list of users.

	if user is already in    users.txt:
		return False

	if user was sucsessfully added to    users.txt:
		return True
	"""
	usersList = get_users_list()
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


def del_user_from_users_list(messageFromUserId):
	"""
	del_user_from_users_list(messageFromUserId)

	Delete user from    users.txt
	messageFromUserId: id of user, that used /sub command.

	Use    get_users_list(params=None)    function to get a list of users.

	if user wasn't found in    users.txt:
		return False

	if user was sucsessfully delited from    users.txt:
		return True
	"""
	usersList = get_users_list()
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


def send_every_day_message():
	"""
	send_every_day_message(params=None)

	This function is a "container", which needed for work of "threading" module.

	Includes:
	send_now(user)
	sending_org(params=None)
	"""
	def send_now(user):
		"""
		send_now(user)

		Send message to specific user.
		
		user: user identificator

		return None
		"""
		serverTimeNow = get_server_data()['time']
		serverDateNow = get_server_data()['date']

		dollarNow = dataDict['dollar']
		euroNow = dataDict['euro']

		ruAll = dataDict['coronaRus']['all']
		ruRecovered = dataDict['coronaRus']['recovered']
		ruDies = dataDict['coronaRus']['dies']

		worldAll = dataDict['coronaWorld']['all']
		worldRecovered = dataDict['coronaWorld']['recovered']
		worldDies = dataDict['coronaWorld']['dies']

		bot.send_message(user, f'Время на сервере {serverTimeNow}.\n\
			\nВот такую информацию мне удалось собрать:\nКурс доллара: {dollarNow}\nКурс евро: {euroNow}\n\
			\nCOVID-19 в России на {serverDateNow}\nВсего случаев: {ruAll}\nВыздоровело: {ruRecovered}\nСмертей: {ruDies}\n\
			\nCOVID-19 в мире:\nВсего случаев: {worldAll}\nВыздоровело: {worldRecovered}\nСмертей: {worldDies}\n\
			\nСпасибо, что подписались на ежедневную рассылку❤️')

		print(f'{serverTimeNow}: ' + 'everyday info message were send to ' + str(user) + ' successfully')
		logging.info(str(user) + ' took everyday info message now')

	def sending_org():
		"""
		sending_org(params=None)

		That's finction-organizer, which I used to send message for every user.
		This function use    get_users_list(params=None)    and call    send_now(user=userList[i]) function.

		return None
		"""
		usersList = get_users_list()

		for i in range(len(usersList)):
			if usersList[i] != '' and usersList[i] != None:
				send_now(usersList[i])

		serverTimeNow = get_server_data()['time']
		print('\n\n' + '#' * 30 + '\nNewsletter is over\n' + '#' * 30 + '\n\n')
		logging.info('\n\n' + '#' * 30 + '\nNewsletter is over\n' + '#' * 30 + '\n\n')

	schedule.every().day.at("13:05").do(sending_org)

	while True:
		schedule.run_pending()
		time.sleep(1)


dataDict = get_new_data()
usersList = []


#	This is information block, that needed for better code navigation	#
#########################################################################
#	|																|	#
#	|	Main block of my bot. Here you can see all commands,		|	#
#	|	that available to users. 									|	#
#	|																|	#
#########################################################################

def bot_body():
	bot = telebot.TeleBot(config.TOKEN)

	print('\n' * 30  + '#' * 30 + '\nNow it\'s started successfully.\nINFO: Server Time:' + get_server_data()['time'] + '\nData Dictionary Parsed successfully.\n' + '#' * 30 + '\n\nData for now:')
	print(pformat(dataDict))
	print('\n\n')
	logging.info('\n\n\n' + '#' * 50 +'\nNow it\'s started successfully.\n' + '#' * 50)


	@bot.message_handler(commands=['start', 'старт', 'начать'])
	def send_welcome_message(message):
		if message.chat.type == 'private':
			serverTimeNow = get_server_data()['time']

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
	def send_help_list(message):
		if message.chat.type == 'private':
			serverTimeNow = get_server_data()['time']

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
	def sub_the_person(message):
		if message.chat.type == 'private':
			serverTimeNow = get_server_data()['time']
			
			print(f'{serverTimeNow}: ' + str(message.from_user.id) + ' used /sub command now')
			logging.info(str(message.from_user.id) + ' used /sub command now')

			feedback = add_user_to_users_list(message.chat.id)

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
	def unfollow_the_person(message):
		if message.chat.type == 'private':
			serverTimeNow = get_server_data()['time']
			
			print(f'{serverTimeNow}: ' + str(message.from_user.id) + ' used /unfollow command now')
			
			logging.info(str(message.from_user.id) + ' used /unfollow command now')
			feedback = del_user_from_users_list(message.chat.id)

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
	def send_report(message):
		if message.chat.type == 'private':
			serverTimeNow = get_server_data()['time']

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
	def send_author_info(message):
		serverTimeNow = get_server_data()['time']

		amountOfUsers = get_followers_amount()

		markup = types.InlineKeyboardMarkup()
		buttonVk = types.InlineKeyboardButton(text='Вконтакте', url='https://vk.com/grnbows')
		buttonInsta = types.InlineKeyboardButton(text='Instagram', url='https://www.instagram.com/grnbows/')
		markup.add(buttonVk, buttonInsta)

		print(f'{serverTimeNow}: ' + str(message.from_user.id) + ' used /author command now')
		logging.info(str(message.from_user.id) + ' used /author command now')

		bot.send_message(message.chat.id, f'Разработчик бота: @grnbows\n\
			\nСо мной можно связаться в Telegram или в других социальных сетях, например ВКонтакте или Instagram. Везде тег такой же - @grnbows.\nТакже у меня есть рабочая почта:\ngrnbows.connect@mail.ru\n\
			\nСпасибо за проявленный интерес к этому проекту, Вы позволяете мне развиваться в программировании дальше.\n\
			\n/donate - для моих реквизитов.\n\
			\nПодписчиков в системе: {amountOfUsers}\nПоследняя актуальная версия бота: {config.__BOT_VESION}', reply_markup = markup)


	@bot.message_handler(commands=['донат', 'помочь', 'donate', 'реквизиты'])
	def send_requisites(message):
		serverTimeNow = get_server_data()['time']

		print(f'{serverTimeNow}: ' + str(message.from_user.id) + ' used /donate command now')
		logging.info(str(message.from_user.id) + ' used /donate command now')

		bot.send_message(message.chat.id, 'Список моих реквизитов недоступен, бот в разработке.\nСпасибо.\
			'.format(message.from_user, bot.get_me()), parse_mode='html')
		bot.send_sticker(message.chat.id, open('images/donate.tgs', 'rb'))


	@bot.message_handler(commands=['info', 'инфо', 'информация'])
	def send_info_now(message):
		if message.chat.type == 'private':
			serverTimeNow = get_server_data()['time']
			serverDateNow = get_server_data()['date']

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


	#	This is information block, that needed for better code navigation	#
	#########################################################################
	#	|																|	#
	#	|	Block of my bot, that allows me send different messages		|	#
	#	|	to my subscribers											|	#
	#	|																|	#
	#########################################################################

	from random import randint


	@bot.message_handler(commands=['sms'])
	def send_message_to_console(message):
		if message.chat.type == 'private':
			chanse = randint(1,10)
			print(message.from_user.first_name + ' - ' + '\'' + message.text[5:len(message.text)] + '\'')
			if chanse <= 2:
				bot.send_photo(message.chat.id, open('images/ktotakie.jpg', 'rb'))
					

	def mail():
		mailText = 'Тест других методов рассылки, просьба не обращать внимания.'

		mailButtons = types.InlineKeyboardMarkup()
		button1 = types.InlineKeyboardButton(text='Вконтакте', url='https://vk.com/grnbows')
		button2 = types.InlineKeyboardButton(text='Instagram', url='https://www.instagram.com/grnbows/')
		mailButtons.add(button1, button2)


		def get_mail_photo(): 
			return open('images/text.jpg', 'rb')


		def send_mail_now(user):
			serverTimeNow = get_server_data()['time']
			
			print(f'{serverTimeNow}: ' + 'mail were send to ' + str(user) + ' successfully')
			logging.info(str(user) + ' took mail now')

			bot.send_photo(user, get_mail_photo(), 
				caption=mailText, 
				parse_mode='html', 
				reply_markup=mailButtons)


		def mail_org():
			usersList = get_users_list()

			for i in range(len(usersList)):
				if usersList[i] != '' and usersList[i] != None:
					send_mail_now(int(usersList[i]))

			print('\n\n' + '#' * 30 + '\nMailing is over\n' + '#' * 30 + '\n\n')
			logging.info('\n\n' + '#' * 30 + '\nMailing is over\n' + '#' * 30 + '\n\n')


		@bot.message_handler(commands=['mail_help'])
		def send_mail_help(message):
			if message.chat.type == 'private' and message.from_user.id == config.ADMIN_ID:
				print('/mail_help used now')
				logging.info('/mail_help used now')

				bot.send_message(config.ADMIN_ID, '\
					<b><i>/mail_test</i></b> - отправить мне тестовое сообщение\n\
					\n<b><i>/mail_start</i></b> - начать рассылку сейчас\
					'.format(message.from_user, bot.get_me()), parse_mode='html')


		@bot.message_handler(commands=['mail_test'])
		def send_test_mail(message):
			if message.chat.type == 'private' and message.from_user.id == config.ADMIN_ID:
				print('/mail_test used now')
				logging.info('/mail_test used now')

				bot.send_photo(config.ADMIN_ID, get_mail_photo(), 
					caption=mailText, 
					parse_mode='html', 
					reply_markup = mailButtons)


		@bot.message_handler(commands=['mail_start'])
		def send_mail_for_all(message):
			if message.chat.type == 'private' and message.from_user.id == config.ADMIN_ID:
				print('/mail_start used now')
				logging.info('/mail_start used now')
				mail_org()


	reloadDataThread = threading.Thread(target=reload_data, name='reloadDataThread')
	sendEveryDayMessageThread = threading.Thread(target=send_every_day_message, name='sendEveryDayMessageThread')
	mailingThread = threading.Thread(target=mail, name='mailingThread')

	sendEveryDayMessageThread.start()
	reloadDataThread.start()
	mailingThread.start()

	while True:
		try:
			bot.polling(none_stop=True, interval=0)
		except: 
			print('bolt')
			time.sleep(5)


if __name__ == '__main__':
	bot_body()