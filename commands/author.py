from commands.message_template import Message_Template
from service_commands import get_followers_amount
from telebot import types
import config

DISABLE_WEB_PAGE_PREVIEW = None # True or False
REPLY_TO_MESSAGE_ID = None
DISABLE_NOTIFICATION = None 
PARSE_MODE = 'html'

COMMAND_TEXT = f'Разработчик бота: @grnbows\n\
			\nСо мной можно связаться в Telegram или в других социальных сетях, например ВКонтакте или Instagram.\nТакже у меня есть рабочая почта:\ngrnbows.connect@mail.ru\n\
			\nСпасибо за проявленный интерес к этому проекту, Вы позволяете мне развиваться в программировании дальше.\n\
			\n/donate - для моих реквизитов.\n\
			\nПодписчиков в системе: {get_followers_amount()}\nПоследняя актуальная версия бота: {config.__BOT_VESION}'


REPLY_MARKUP = types.InlineKeyboardMarkup(row_width=1)

donate_button = types.InlineKeyboardButton(text='Посмотреть реквизиты', callback_data='donate')
vk_button = types.InlineKeyboardButton(text='Вконтакте', url='https://vk.com/grnbows')
insta_button = types.InlineKeyboardButton(text='Instagram', url='https://www.instagram.com/grnbows/')
help_button = types.InlineKeyboardButton(text='Список команд', callback_data='help')

REPLY_MARKUP.add(donate_button, vk_button, insta_button, help_button)


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
