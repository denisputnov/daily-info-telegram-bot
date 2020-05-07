from commands.message_template import Message_Template
from telebot import types
from service_commands import get_users_list
from service_commands import get_server_data
from service_commands import dataDict


serverTimeNow = get_server_data()['time']
serverDateNow = get_server_data()['date']

dollarNow = dataDict['dollar']
euroNow = dataDict['euro']

ruAll = dataDict['coronaRus']['all']
ruRecovered = dataDict['coronaRus']['recovered']
ruDies = dataDict['coronaRus']['dies']
ruPlus = dataDict['coronaRus']['plus']

worldAll = dataDict['coronaWorld']['all']
worldRecovered = dataDict['coronaWorld']['recovered']
worldDies = dataDict['coronaWorld']['dies']



DISABLE_WEB_PAGE_PREVIEW = None # True or False
REPLY_TO_MESSAGE_ID = None
DISABLE_NOTIFICATION = None 
PARSE_MODE = 'html'

COMMAND_TEXT = f'Время на сервере {serverTimeNow}.\n\
				\nВот такую информацию мне удалось собрать:\nКурс доллара: {dollarNow}\nКурс евро: {euroNow}\n\
				\nCOVID-19 в России на {serverDateNow}\nВсего случаев: {ruAll} (+{ruPlus})\nВыздоровело: {ruRecovered}\nСмертей: {ruDies}\n\
				\nCOVID-19 в мире:\nВсего случаев: {worldAll}\nВыздоровело: {worldRecovered}\nСмертей: {worldDies}'

REPLY_MARKUP_FOLLOWED = types.InlineKeyboardMarkup(row_width=1)
REPLY_MARKUP_UNFOLLOWED = types.InlineKeyboardMarkup(row_width=1)
CALLBACK_MARKUP_FOLLOWED = types.InlineKeyboardMarkup(row_width=1)
CALLBACK_MARKUP_UNFOLLOWED = types.InlineKeyboardMarkup(row_width=1)

help_button = types.InlineKeyboardButton(text='Список команд', callback_data='help')
sub_button = types.InlineKeyboardButton(text='Подписаться на рассылку', callback_data='sub')
unfollow_button = types.InlineKeyboardButton(text='Отписаться', callback_data='unfollow')
picture_button = types.InlineKeyboardButton(text='Посмотреть визуализацию для России', callback_data='picture')
info_button = types.InlineKeyboardButton(text='Показать информацию', callback_data='info')
info_button_callback = types.InlineKeyboardButton(text='Скрыть график', callback_data='info')


REPLY_MARKUP_FOLLOWED.add(picture_button, help_button, unfollow_button)
REPLY_MARKUP_UNFOLLOWED.add(picture_button, help_button, sub_button)
CALLBACK_MARKUP_FOLLOWED.add(info_button_callback, help_button, unfollow_button)
CALLBACK_MARKUP_UNFOLLOWED.add(info_button_callback, help_button, sub_button)

def construct_markup(message_chat_id):
	usersList = get_users_list()
	if str(message_chat_id) in usersList:
		return CALLBACK_MARKUP_FOLLOWED
	else:
		return CALLBACK_MARKUP_UNFOLLOWED

def construct_message(message_chat_id):
	usersList = get_users_list()
	if str(message_chat_id) in usersList:
		message = Message_Template(
				chat_id = message_chat_id,
				text = COMMAND_TEXT, 

				disable_web_page_preview=DISABLE_WEB_PAGE_PREVIEW,
				reply_to_message_id=REPLY_TO_MESSAGE_ID, 
				reply_markup=REPLY_MARKUP_FOLLOWED,
				parse_mode=PARSE_MODE, 
				disable_notification=DISABLE_NOTIFICATION, 
				timeout=None
			)
		return message
	else:
		message = Message_Template(
				chat_id = message_chat_id,
				text = COMMAND_TEXT, 

				disable_web_page_preview=DISABLE_WEB_PAGE_PREVIEW,
				reply_to_message_id=REPLY_TO_MESSAGE_ID, 
				reply_markup=REPLY_MARKUP_UNFOLLOWED,
				parse_mode=PARSE_MODE, 
				disable_notification=DISABLE_NOTIFICATION, 
				timeout=None
			)
		return message
