import time

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import requests
from bs4 import BeautifulSoup
import csv

import string

URL = 'https://www.fonbet.ru/bets/football/'
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36', 'accept':'*/*'} 
FILE = 'fonbet.csv'

def has_no_class(tag):
    return not tag.has_attr('class')

def get_html(driver):
	element = driver.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "table__row")))
	html = driver.page_source
	return html


def get_content(html):
	soup = BeautifulSoup(html,'html.parser')
	matches = [] 
	table = soup.find('table',class_='table')
	desks = table.find_all('tbody',class_='table__body')
	print("Кря_desks:",len(desks))
	i = 1
	for desk in desks:
		#print("	Кря_desk_"+str(i))
		i = i+1
		comp = ""
		rows = desk.find_all('tr',class_='table__row')
		#print("		Кря_rows:",len(rows))
		for row in rows:
			if row == rows[0]:
				headline = row.find("th")
				if headline != None:
					comp = headline.find("h2",class_='table__title-text').get_text(strip=True)
					print('	Кря_comp: '+comp)
			else:
				notmatch = row.find('td',class_='table-complex__wrap')
				if notmatch == None:
					bothteams = row.find('h3',class_='table__match-title-text').get_text(strip=True)
					#print('		Кря: '+bothteams)
					team1 = bothteams[:bothteams.find(' — ')]
					team2 = bothteams[bothteams.find(' — ')+3:]
					#print('		Кря_teams: '+team1+' : '+team2)
					datetime = row.find('div',class_='table__time')
					str_datetime = datetime.find(has_no_class).get_text(strip=True)
					str_date = str_datetime[:str_datetime.find(' в ')]
					str_time = str_datetime[str_datetime.find(' в ')+3:]
					coefs = row.find_all('td',class_='_type_btn',limit=3)
					try:
						c1 = float(coefs[0].get_text(strip=True))
						cX = float(coefs[1].get_text(strip=True))
						c2 = float(coefs[2].get_text(strip=True))
					except ValueError:
						print('		Кря_game:',team1,'vs',team2,'|',str_date,str_time,'|','нет коэффициентов')
					else:
						print('		Кря_game:',team1,'vs',team2,'|',str_date,str_time,'|',c1,'|',cX,'|',c2)


	'''
	items = desk.find_all('div', class_='tg__match_header') #список матчей на сайте

	itteams = desk.find_all('div',class_='prematch_name') #cписок названий команд на сайте
	teams = [] #список названий команд
	for team in itteams:
		teams.append(team.get_text(strip=True))	#текст
	
	itcoef = desk.find_all('div',class_='prematch_stake_odd_factor') #cписок коэффициентов матчей на сайте tg--mar-r-8
	coefs = []#cписок коэффициентов матчей
	for coef in itcoef:
		coefs.append(coef.get_text(strip=True))	#текст

	itdatetime = desk.find

	matches = []
	i=0
	j=0
	for item in items:
		matches.append({
			'date':item.find('div',class_='bui-event-row__date-d4666b').get_text(strip =True),
			'time':item.find('span',class_='bui-event-row__time-a6eb59').get_text(strip =True),
			'team1':teams[i],
			'team2':teams[i+1],
			'k1':coefs[j],
			'kx':coefs[j+1],
			'k2':coefs[j+2]
		})
		i = i + 2
		j += 3
	#print(matches)
	#print(len(matches))
	'''
	return matches

def save_file(items,path):
	with open(path,'w',newline='') as file:
			writer = csv.writer(file,delimiter=';')
			writer.writerow(['Дата','Время','Команда 1','Команда 2','1', 'Х', '2'])
			for item in items:
				writer.writerow([item['date'],item['time'],item['team1'],item['team2'],item['k1'], item['kx'], item['k2']])

def init_driver():
    driver = webdriver.Chrome('C:\\webdrivers\\chromedriver.exe')
    driver.wait = WebDriverWait(driver, 10)
    return driver

def parse():
	driver = init_driver()
	try:
		driver.get(URL) 
		html = get_html(driver)
		#print('Кря_html:',html)				
		get_content(html)
	finally:
		#time.sleep(2)
		print('Кря_совсем_конец')
		driver.quit()

def main():
	parse()

if __name__ == '__main__':
	main()