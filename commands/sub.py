from commands.message_template import Message_Template
from telebot import types
from service_commands import add_user_to_users_list
from service_commands import usersList


DISABLE_WEB_PAGE_PREVIEW = None # True or False
REPLY_TO_MESSAGE_ID = None
DISABLE_NOTIFICATION = None 
PARSE_MODE = 'html'

COMMAND_TEXT_POS = 'Подписка на ежедневную рассылку успешно оформлена.'
COMMAND_TEXT_NEG = 'Вы уже подписаны на рассылку, повторная подписка невозможна.\nБот ошибается? /report.'


help_button = types.InlineKeyboardButton(text='Список команд', callback_data='help')
info_button = types.InlineKeyboardButton(text='Показать информацию', callback_data='info')
report_button = types.InlineKeyboardButton(text='Сообщить об ошибке', callback_data='report')

REPLY_MARKUP_POS = types.InlineKeyboardMarkup(row_width=1)
REPLY_MARKUP_POS.add(info_button, help_button)
REPLY_MARKUP_NEG = types.InlineKeyboardMarkup(row_width=1)
REPLY_MARKUP_NEG.add(report_button, help_button)


def construct_message(message_chat_id):
	if add_user_to_users_list(message_chat_id):

		message = Message_Template(
				chat_id = message_chat_id,
				text = COMMAND_TEXT_POS, 

				disable_web_page_preview=DISABLE_WEB_PAGE_PREVIEW,
				reply_to_message_id=REPLY_TO_MESSAGE_ID, 
				reply_markup=REPLY_MARKUP_POS,
				parse_mode=PARSE_MODE, 
				disable_notification=DISABLE_NOTIFICATION, 
				timeout=None
			)
		return message
	else:
		message = Message_Template(
				chat_id = message_chat_id,
				text = COMMAND_TEXT_NEG, 

				disable_web_page_preview=DISABLE_WEB_PAGE_PREVIEW,
				reply_to_message_id=REPLY_TO_MESSAGE_ID, 
				reply_markup=REPLY_MARKUP_NEG,
				parse_mode=PARSE_MODE, 
				disable_notification=DISABLE_NOTIFICATION, 
				timeout=None
			)
		return message

