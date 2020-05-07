from commands.message_template import Message_Template
from telebot import types
from service_commands import get_users_list


DISABLE_WEB_PAGE_PREVIEW = None # True or False
REPLY_TO_MESSAGE_ID = None
DISABLE_NOTIFICATION = None 
PARSE_MODE = 'html'

COMMAND_TEXT = 'Список доступных команд:'

REPLY_MARKUP_FOLLOWED = types.InlineKeyboardMarkup(row_width=1)
REPLY_MARKUP_UNFOLLOWED = types.InlineKeyboardMarkup(row_width=1)

info_button = types.InlineKeyboardButton(text='Показать информацию', callback_data='info')
sub_button = types.InlineKeyboardButton(text='Подписаться на рассылку', callback_data='sub')
unfollow_button = types.InlineKeyboardButton(text='Отписаться', callback_data='unfollow')
report_button = types.InlineKeyboardButton(text='Сообщить об ошибке', callback_data='report')
author_button = types.InlineKeyboardButton(text='Об авторе', callback_data='author')

REPLY_MARKUP_FOLLOWED.add(info_button, unfollow_button, report_button, author_button)
REPLY_MARKUP_UNFOLLOWED.add(info_button, sub_button, report_button, author_button)

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
