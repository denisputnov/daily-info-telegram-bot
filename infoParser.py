import config 
import requests
from bs4 import BeautifulSoup as bs


def checkDollarValue():
	dollarFullPage = requests.get(config.DOLLAR_RUB, headers=config.headers)
	dollarSoup = bs(dollarFullPage.content, 'html.parser')
	dollarConvert = dollarSoup.findAll('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})
	return dollarConvert[0].text


def checkEuroValue():
	euroFullPage = requests.get(config.EURO_RUB, headers=config.headers)
	euroSoup = bs(euroFullPage.content, 'html.parser')
	euroConvert = euroSoup.findAll('span', {'class': 'DFlfde', 'class': 'SwHCTb', 'data-precision': 2})
	return euroConvert[0].text


def checkCoronaRussia():
	coronaRusiiaFullPage = requests.get(config.CORONA_RUSSIA, headers=config.headers)
	coronaRussiaSoup = bs(coronaRusiiaFullPage.content, 'html.parser')
	coronaRussiaConvert = coronaRussiaSoup.findAll('b')
	return {'all': coronaRussiaConvert[0].text, 'recovered': coronaRussiaConvert[1].text, 'dies': coronaRussiaConvert[2].text}


def checkCoronaWorld():
	coronaWorldFullPage = requests.get(config.CORONA_WORLD, headers=config.headers)
	coronaWorldSoup = bs(coronaWorldFullPage.content, 'html.parser')
	coronaWorldConvert = coronaWorldSoup.findAll('div', {'class': 'value', 'class': 'js-confirmed-value'})
	return coronaWorldConvert
