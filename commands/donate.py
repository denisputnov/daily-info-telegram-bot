from commands.message_template import Message_Template
from telebot import types
import config
from service_commands import get_followers_amount

DISABLE_WEB_PAGE_PREVIEW = None # True or False
REPLY_TO_MESSAGE_ID = None
DISABLE_NOTIFICATION = None 
PARSE_MODE = 'html'

COMMAND_TEXT = 'Вот номер моей карты и кошёльки:\n\
			\nСбербанк: 4274320030073988\nWMR: R591990296871\n\
			\nСпасибо.'


REPLY_MARKUP = types.InlineKeyboardMarkup(row_width=1)

qivi_button = types.InlineKeyboardButton(text='QIVI', url='https://qiwi.com/n/GRNBOWS')
help_button = types.InlineKeyboardButton(text='Список команд', callback_data='help')

REPLY_MARKUP.add(qivi_button, help_button)


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
