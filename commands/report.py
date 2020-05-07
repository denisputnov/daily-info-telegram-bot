from commands.message_template import Message_Template
from telebot import types

DISABLE_WEB_PAGE_PREVIEW = None # True or False
REPLY_TO_MESSAGE_ID = None
DISABLE_NOTIFICATION = None 
PARSE_MODE = 'html'

COMMAND_TEXT = f'Сообщить о работе бота можно @grnbows в личных сообщениях Telegram по следующей форме:\n\
				\n1. Примерное время возникновения ошибки.\n2. Скрин места переписки, где наглядно видна ошибка.\n3. Краткое описание проблемы своими словами.\n4. Скрин/переслать это сообщение.\n\
				\nСпасибо за помощь в разработке бота. Ваши отзывы очень помогают разобраться в проблеме.\n'


REPLY_MARKUP = types.InlineKeyboardMarkup(row_width=1)

help_button = types.InlineKeyboardButton(text='Список команд', callback_data='help')

REPLY_MARKUP.add(help_button)


def construct_message(message_chat_id):
	message = Message_Template(
			chat_id = message_chat_id,
			text = COMMAND_TEXT, 

			disable_web_page_preview=DISABLE_WEB_PAGE_PREVIEW,
			reply_to_message_id=REPLY_TO_MESSAGE_ID, 
			reply_markup=REPLY_MARKUP,
			parse_mode=PARSE_MODE, 
			disable_notification=DISABLE_NOTIFICATION, 
			timeout=None
		)
	return message
