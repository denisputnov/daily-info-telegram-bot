import config 
import requests
from bs4 import BeautifulSoup as bs


def reformate(value):
	value = str(value)
	if len(value) > 9:
		return value[0:len(value) - 9] + '.' + value[len(value) - 9:len(value) - 6] + '.' + value[len(value) - 6:len(value) - 3] + '.' + value[len(value) - 3: len(value)]
	elif len(value) > 6:
		return value[0:len(value) - 6] + '.' + value[len(value) - 6:len(value) - 3] + '.' + value[len(value) - 3:len(value)]
	elif len(value) > 3:
		return value[0:len(value) - 3] + '.' + value[len(value) - 3:len(value)]
	elif len(value) > 0:
		return value


def checkDollarValue():
	dollarFullPage = requests.get(config.DOLLAR_RUB, headers=config.headers)
	dollarSoup = bs(dollarFullPage.content, 'html.parser')
	dollarConvert = dollarSoup.findAll('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})
	return dollarConvert[0].text.replace(',','.')


def checkEuroValue():
	euroFullPage = requests.get(config.EURO_RUB, headers=config.headers)
	euroSoup = bs(euroFullPage.content, 'html.parser')
	euroConvert = euroSoup.findAll('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})
	return euroConvert[0].text.replace(',','.')


def checkCoronaRussia():
	coronaRusiiaFullPage = requests.get(config.CORONA_RUSSIA, headers=config.headers)
	coronaRussiaSoup = bs(coronaRusiiaFullPage.content, 'html.parser')
	coronaRussiaConvert = coronaRussiaSoup.findAll('b')
	# if __name__ == '__main__':
	# 	print(coronaRussiaConvert)
	return {'all': reformate(coronaRussiaConvert[0].text), 
			'recovered': reformate(coronaRussiaConvert[1].text), 
			'dies': reformate(coronaRussiaConvert[3].text)}


def checkCoronaWorld():
	coronaWorldFullPage = requests.get(config.CORONA_WORLD, headers=config.headers)
	coronaWorldSoup = bs(coronaWorldFullPage.content, 'html.parser')
	coronaWorldConvert = coronaWorldSoup.findAll('div', {'class': 'maincounter-number'})
	# if __name__ == '__main__':
		# print(coronaWorldConvert[0].text.replace('\n',''))
	return {'all': reformate(coronaWorldConvert[0].text.replace(' ','').replace('\n','').replace(',','')), 
			'recovered': reformate(coronaWorldConvert[2].text.replace(' ','').replace('\n','').replace(',','')), 
			'dies': reformate(coronaWorldConvert[1].text.replace(' ','').replace('\n','').replace(',',''))}


if __name__ == '__main__':
	# print(checkDollarValue())
	# print(checkEuroValue())
	# print(checkCoronaWorld())
	# print(checkCoronaRussia())
	while True:
		print(reformate(input()))
