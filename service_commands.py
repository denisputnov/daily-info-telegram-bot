"""
Service commands, whitch need for bot's work
"""
import time
import threading

from pprint import pformat

import dataParser
import config
import graph




def get_server_data():
	"""
	get_server_data(params=None)

	return dictionary {'time': serverTime,'date': serverDate}
	"""
	serverTime = str(((int(time.strftime('%H'))) + 3) % 24) + ':' + time.strftime('%M:%S (UTC +3)')
	serverDate = time.strftime('%d.%m.20%y')
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

	return {'dollar': dollarNow, 
			'euro': euroNow,
			'coronaRus': {
				'all': ruCorona['all'], 
				'recovered': ruCorona['recovered'],
				'dies': ruCorona['dies'],
				'plus': ruCorona['plus']},
			'coronaWorld': {
				'all': worldCorona['all'], 
				'recovered': worldCorona['recovered'],
				'dies': worldCorona['dies'] }
			}


dataDict = get_new_data()
usersList = []

def get_graph():
	return graph.draw_graph(data=dataParser.get_corona_ru_per_day(), width=1000, height=500, show_values=False, watermark_text='Telegram | @pyInfoParserBot')


def get_users_list():
	"""
	get_users_list(params=None)

	return all user identificators from    users.txt    as list.
	"""
	global usersList
	with open('users.txt', 'r') as file:
		usersList = file.read().split(' ')
	usersList = list(filter(lambda a: a != '', usersList))
	return usersList


def get_followers_amount():
	"""
	get_followers_amount(params=None)
	
	return len(get_users_list(params=None))
	"""
	return len(get_users_list())

def add_user_to_users_list(message_from_user_id):
	"""
	add_user_to_users_list(message_from_user_id)
	
	Add user to 	file-/database-name
	message_from_user_id: id of user, that used ***/sub*** command.
	
	Use    get_users_list(params=None)    function to get a list of users.

	if user is already in    file-/database-name:
		return False

	if user was sucsessfully added to    file-/database-name:
		return True
	"""
	global usersList
	usersList = get_users_list()
	if str(message_from_user_id) in usersList:
		return False
	else:
		with open('users.txt', 'a') as file:
			file.write(str(message_from_user_id) + ' ')
		print(f'{message_from_user_id} was added to the list successfully')
		return True

def del_user_from_users_list(message_from_user_id):
	"""
	del_user_from_users_list(message_from_user_id)

	Delete user from    users.txt
	message_from_user_id: id of user, that used ***/unfollow*** command.

	Use    get_users_list(params=None)    function to get a list of users.

	if user wasn't found in    ufile-/database-name:
		return False

	if user was sucsessfully delited from    file-/database-name:
		return True
	"""
	usersList = get_users_list()
	if str(message_from_user_id) in usersList:
		usersList.remove(str(message_from_user_id))
		with open('users.txt', 'w') as file:
			stroke = ' '.join(usersList) + ' '
			file.write(stroke)
		stroke = ''
		print(f'{message_from_user_id} was deleted from the list successfully')
		return True
	else:
		return False

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

if __name__ == '__main__':
	get_graph()

if __name__ != '__main__':
	get_users_list()
	reloadDataThread = threading.Thread(target=reload_data, name='reloadDataThread')
	reloadDataThread.start()
