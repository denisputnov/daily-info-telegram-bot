"""
EN: 
Telegram interface for checking dollar and euro course to ruble
and check COVID-19 situation in Russia and all over the world.

RU:
Телеграмм бот для отслеживания курса доллара и евро к рублю
и проверки ситуации коронавируса в России и по всему миру.

Use    python bot.py    command to start.

Params: None

Copyright © 2020 Denis Putnov. All rights reserved.
"""

import telebot
import time
import threading
import schedule

from pprint import pformat
from telebot import types

import dataParser
import config

from service_commands import get_server_data
from service_commands import get_new_data
from service_commands import get_users_list
from service_commands import get_followers_amount
from service_commands import add_user_to_users_list
from service_commands import del_user_from_users_list
from service_commands import get_graph

from service_commands import dataDict
from service_commands import usersList

from commands import help
from commands import start
from commands import info
from commands import sub
from commands import unfollow
from commands import author
from commands import report
from commands import donate


if __name__ == '__main__':
	
	get_graph()

	bot = telebot.TeleBot(config.TOKEN)

	@bot.callback_query_handler(func=lambda call: True)
	def send_inline_callback(call):
		try:
			if call.message:
				if call.data == 'help':
					try:
						params = help.construct_message(call.message.chat.id)
						bot.edit_message_text(chat_id=call.message.chat.id, 
							message_id=call.message.message_id,
							text=params.text, 
							reply_markup=params.reply_markup)
					except Exception as e:
						bot.delete_message(chat_id=call.message.chat.id,
							message_id=call.message.message_id)
						send_help_message(call.message)

				elif call.data == 'info':
					try:
						params = info.construct_message(call.message.chat.id)
						bot.edit_message_text(chat_id=call.message.chat.id,
							message_id=call.message.message_id,
							text=params.text,
							reply_markup=params.reply_markup)
					except Exception as e:
						bot.delete_message(chat_id=call.message.chat.id,
							message_id=call.message.message_id)
						send_info_message(call.message)

				elif call.data == 'sub':
					try:
						params = sub.construct_message(call.message.chat.id)
						bot.edit_message_text(chat_id=call.message.chat.id,
							message_id=call.message.message_id,
							text=params.text,
							reply_markup=params.reply_markup)

						bot.send_message(config.ADMIN_ID, 'Кто-то подписался/отписался\n\n' +' '.join(get_users_list()))
					
					except Exception as e:
						bot.send_message(config.ADMIN_ID, 'Какая-то ошибка в блоке try/except у SUB, надо исправить.')
						params = sub.construct_message(call.message.chat.id)
						bot.delete_message(chat_id=call.message.chat.id,
							message_id=call.message.message_id)
						send_sub_message(call.message)

				elif call.data == 'unfollow':
					try:
						params = unfollow.construct_message(call.message.chat.id)
						bot.edit_message_text(chat_id=call.message.chat.id,
							message_id=call.message.message_id,
							text=params.text,
							reply_markup=params.reply_markup)

						bot.send_message(config.ADMIN_ID, 'Кто-то подписался/отписался\n\n' +' '.join(get_users_list()))

					except Exception as e:
						bot.send_message(config.ADMIN_ID, 'Какая-то ошибка в блоке try/except у UNFOLLOW, надо исправить.')
						params = unfollow.construct_message(call.message.chat.id)
						bot.delete_message(chat_id=call.message.chat.id,
							message_id=call.message.message_id)
						send_sub_message(call.message)

				elif call.data == 'report':
					try:
						params = report.construct_message(call.message.chat.id)
						bot.edit_message_text(chat_id=call.message.chat.id,
							message_id=call.message.message_id,
							text=params.text + f'\n\nmessage.chat.id - {call.message.chat.id}\nmessage.from_user.id - {call.message.from_user.id}\nmessage.chat.type - {call.message.chat.type}',
							reply_markup=params.reply_markup)

					except Exception as e:
						params = report.construct_message(call.message.chat.id)
						bot.delete_message(chat_id=call.message.chat.id,
							message_id=call.message.message_id)
						send_report_message(call.message)

				elif call.data == 'author':
					try:
						params = author.construct_message(call.message.chat.id)
						bot.edit_message_text(chat_id=call.message.chat.id,
							message_id=call.message.message_id,
							text=params.text,
							reply_markup=params.reply_markup)

					except Exception as e:
						params = author.construct_message(call.message.chat.id)
						bot.delete_message(chat_id=call.message.chat.id,
							message_id=call.message.message_id)
						send_report_message(call.message)

				elif call.data == 'donate':
					try:
						bot.delete_message(chat_id=call.message.chat.id,
							message_id=call.message.message_id)
						send_report_message(call.message)

					except Exception as e:
						bot.edit_message_text(chat_id=call.message.chat.id, 
							message_id=call.message.message_id,
							text='Кажется, произошла какая=то ошибка. Используйте команду /report, чтобы сообщить',
							reply_markup=report.construct_message(call.message.chat.id).reply_markup)

				elif call.data == 'picture':
					try:
						params = info.construct_message(call.message.chat.id)
						bot.delete_message(chat_id=call.message.chat.id,
							message_id=call.message.message_id)
						CALLBACK_MARKUP = info.construct_markup(call.message.chat.id)
						bot.send_photo(chat_id=call.message.chat.id, 
							caption=params.text,
							photo=open('out.jpeg', 'rb'),
							reply_markup=CALLBACK_MARKUP)
					except Exception as e:
						print(repr(e))
						bot.send_message(config.ADMIN_ID, 'Какая-то ошибка с callback методом picture')

		except Exception as e:
			print(repr(e))

	@bot.message_handler(commands=['start', 'старт', 'начать'])
	def send_start_message(message):
		try:
			params = start.construct_message(message.chat.id)
			bot.send_message(chat_id=params.chat_id,
				text=params.text[0],
				parse_mode=params.parse_mode)
			bot.send_message(chat_id=params.chat_id,
				text=params.text[1],
				parse_mode=params.parse_mode)
			bot.send_message(chat_id=params.chat_id,
				text=params.text[2],
				parse_mode=params.parse_mode,
				reply_markup=params.reply_markup)
			
		except AttributeError as e:
			print(repr(e))
			bot.send_message(chat_id=message.chat.id, text='Эта команда в данный момент недоступна.')


	@bot.message_handler(commands=['help', 'commands', 'помощь'])
	def send_help_message(message):
		try:
			params = help.construct_message(message.chat.id)
			bot.send_message(chat_id=params.chat_id,
				text=params.text,
				parse_mode=params.parse_mode,
				reply_markup=params.reply_markup)

		except AttributeError as e:
			print(repr(e))
			bot.send_message(chat_id=message.chat.id, text='Эта команда в данный момент недоступна.')
	

	@bot.message_handler(commands=['info', 'инфо', 'информация'])
	def send_info_message(message):
		try:
			params = info.construct_message(message.chat.id)
			bot.send_message(chat_id=params.chat_id,
				text=params.text,
				parse_mode=params.parse_mode,
				reply_markup=params.reply_markup)

		except AttributeError as e:
			print(repr(e))
			bot.send_message(chat_id=message.chat.id, text='Эта команда в данный момент недоступна.')


	@bot.message_handler(commands=['записаться', 'регулярно', 'sub', 'subscribe'])
	def send_sub_message(message):
		try:
			params = sub.construct_message(message.chat.id)
			bot.send_message(chat_id=params.chat_id,
				text=params.text,
				parse_mode=params.parse_mode,
				reply_markup=params.reply_markup)

			bot.send_message(config.ADMIN_ID, ' '.join(get_users_list()))

		except AttributeError as e:
			print(repr(e))
			bot.send_message(chat_id=message.chat.id, text='Эта команда в данный момент недоступна.')


	@bot.message_handler(commands=['отписаться', 'unfollow', 'unf', 'unsub'])
	def send_sub_message(message):
		try:
			params = unfollow.construct_message(message.chat.id)
			bot.send_message(chat_id=params.chat_id,
				text=params.text,
				parse_mode=params.parse_mode,
				reply_markup=params.reply_markup)

			bot.send_message(config.ADMIN_ID, ' '.join(get_users_list()))

		except AttributeError as e:
			print(repr(e))
			bot.send_message(chat_id=message.chat.id, text='Эта команда в данный момент недоступна.')

	@bot.message_handler(commands=['report', 'ошибка', 'баг'])
	def send_report_message(message):
		try:
			params = report.construct_message(message.chat.id)
			bot.send_message(chat_id=params.chat_id,
				text=params.text,
				parse_mode=params.parse_mode,
				reply_markup=params.reply_markup)

		except AttributeError as e:
			print(repr(e))
			bot.send_message(chat_id=message.chat.id, text='Эта команда в данный момент недоступна.')

	@bot.message_handler(commands=['автор', 'grnbows', 'разработчик', 'программист', 'author', 'заказать'])
	def send_author_message(message):
		try:
			params = author.construct_message(message.chat.id)
			bot.send_message(chat_id=params.chat_id,
				text=params.text,
				parse_mode=params.parse_mode,
				reply_markup=params.reply_markup)

		except AttributeError as e:
			print(repr(e))
			bot.send_message(chat_id=message.chat.id, text='Эта команда в данный момент недоступна.')

	@bot.message_handler(commands=['донат', 'помочь', 'donate', 'реквизиты'])
	def send_report_message(message):
		try:
			bot.send_sticker(message.chat.id, open('images/donate.tgs', 'rb'))
			params = donate.construct_message(message.chat.id)
			bot.send_message(chat_id=params.chat_id,
				text=params.text,
				parse_mode=params.parse_mode,
				reply_markup=params.reply_markup)

		except AttributeError as e:
			print(repr(e))
			bot.send_message(chat_id=message.chat.id, text='Эта команда в данный момент недоступна.')










	def send_every_day_message():
		def send_now(user):
			params = info.construct_message(user)
			bot.send_message(chat_id=params.chat_id,
				text=params.text + '\nСпасибо, что подписались на ежедневную рассылку❤️',
				reply_markup=params.reply_markup)

		def sending_org():
			usersList = get_users_list()

			for i in range(len(usersList)):
				if usersList[i] != '' and usersList[i] != None:
					send_now(usersList[i])

			serverTimeNow = get_server_data()['time']

		schedule.every().day.at(config.MAIL_TIME).do(sending_org)

		while True:
			schedule.run_pending()
			time.sleep(1)

	if __name__ == '__main__':
		sendEveryDayMessageThread = threading.Thread(target=send_every_day_message, name='sendEveryDayMessageThread')
		sendEveryDayMessageThread.start()










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
			bot.send_photo(user, get_mail_photo(), 
				caption=mailText, 
				parse_mode='html', 
				reply_markup=mailButtons)


		def mail_org():
			usersList = get_users_list()
			for i in range(len(usersList)):
				if usersList[i] != '' and usersList[i] != None:
					send_mail_now(int(usersList[i]))


		@bot.message_handler(commands=['mail_help'])
		def send_mail_help(message):
			if message.chat.type == 'private' and message.from_user.id == config.ADMIN_ID:
				bot.send_message(config.ADMIN_ID, '\
					<b><i>/mail_test</i></b> - отправить мне тестовое сообщение\n\
					\n<b><i>/mail_start</i></b> - начать рассылку сейчас', parse_mode='html')


		@bot.message_handler(commands=['mail_test'])
		def send_test_mail(message):
			if message.chat.type == 'private' and message.from_user.id == config.ADMIN_ID:
				bot.send_photo(config.ADMIN_ID, get_mail_photo(), 
					caption=mailText, 
					parse_mode='html', 
					reply_markup=mailButtons)


		@bot.message_handler(commands=['mail_start'])
		def send_mail_for_all(message):
			if message.chat.type == 'private' and message.from_user.id == config.ADMIN_ID:
				mail_org()

	if __name__ == '__main__':
		mailingThread = threading.Thread(target=mail, name='mailingThread')
		mailingThread.start()










	while True:
		try:
			bot.polling(none_stop=True, interval=0)
		except: 
			print('Connection failed')
			time.sleep(5)
