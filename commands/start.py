from commands.message_template import Message_Template
from config import MAIL_TIME
from telebot import types
from service_commands import get_users_list

DISABLE_WEB_PAGE_PREVIEW = None # True or False
REPLY_TO_MESSAGE_ID = None
DISABLE_NOTIFICATION = None 
PARSE_MODE = 'html'

COMMAND_TEXT_ONE = 'Привет! Я отправлю тебе краткую сводку самых важных новостей на день.\n\nНа сегодня актуально:\n•Курс доллара и евро\n•Ситуация COVID-19 в России и мире\n'
COMMAND_TEXT_TWO = 'Подпишись на рассылку, чтобы получать информацию автоматически каждый день в 13:00 по МСК (UTC +3).'
COMMAND_TEXT_THREE = 'Хочешь узнать больше? Открой список команд.'

REPLY_MARKUP_FOLLOWED = types.InlineKeyboardMarkup(row_width=1)
REPLY_MARKUP_UNFOLLOWED = types.InlineKeyboardMarkup(row_width=1)

help_button = types.InlineKeyboardButton(text='Список команд', callback_data='help')
info_button = types.InlineKeyboardButton(text='Показать информацию', callback_data='info')
sub_button = types.InlineKeyboardButton(text='Подписаться', callback_data='sub')
unfollow_button = types.InlineKeyboardButton(text='Отписаться', callback_data='unfollow')

REPLY_MARKUP_UNFOLLOWED.add(help_button, info_button, sub_button)
REPLY_MARKUP_FOLLOWED.add(help_button, info_button, unfollow_button)

def construct_message(message_chat_id):
	usersList = get_users_list()
	if str(message_chat_id) in usersList:
		message = Message_Template(
				chat_id = message_chat_id,
				text = (COMMAND_TEXT_ONE, COMMAND_TEXT_TWO, COMMAND_TEXT_THREE), 

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
				text = (COMMAND_TEXT_ONE, COMMAND_TEXT_TWO, COMMAND_TEXT_THREE), 

				disable_web_page_preview=DISABLE_WEB_PAGE_PREVIEW,
				reply_to_message_id=REPLY_TO_MESSAGE_ID, 
				reply_markup=REPLY_MARKUP_UNFOLLOWED,
				parse_mode=PARSE_MODE, 
				disable_notification=DISABLE_NOTIFICATION, 
				timeout=None
			)
		return message
