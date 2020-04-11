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

import pytz, datetime
from datetime import date
from datetime import time
from datetime import timedelta
from datetime import datetime, timezone

def local_to_utc(local_datetime):
	local = pytz.timezone ("Europe/Moscow")
	naive = local_datetime
	local_dt = local.localize(naive, is_dst=None)
	utc_dt = local_dt.astimezone(pytz.utc)
	return utc_dt

def int_month(str_month):
	if str_month == 'января':
		return 1
	if str_month == 'февраля':
		return 2
	if str_month == 'марта':
		return 3
	if str_month == 'апреля':
		return 4 
	if str_month == 'мая':
		return 5
	if str_month == 'июня':
		return 6
	if str_month == 'июля':
		return 7
	if str_month == 'августа':
		return 8
	if str_month == 'сентября':
		return 9
	if str_month == 'октября':
		return 10
	if str_month == 'ноября':
		return 11
	if str_month == 'декабря':
		return 12

def format_date(str_date):
	d = date.today()
	if str_date == 'Сегодня':
		pass
	else:
		if str_date == 'Завтра':
			delta = timedelta(days=1)
			#print('Кря_+1')
			d = d + delta
		else:
			str_day = str_date[:str_date.find(' ')]
			day = int(str_day)
			str_month = str_date[str_date.find(' ')+1:]
			month = int_month(str_month)
			year = d.year
			d = date(year,month,day)
	return d

def format_time(str_time):
	hours = int(str_time[:str_time.find(':')])
	minutes = int(str_time[str_time.find(':')+1:])
	t = timedelta(hours=hours,minutes=minutes)
	return t

def format_datetime(str_date,str_time):
	d = format_date(str_date)
	t = format_time(str_time)
	dt = datetime(year=d.year,month=d.month,day=d.day)
	dt = dt + t
	dt = local_to_utc(dt)
	dt = utc_to_local(dt)
	return dt
	

def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def has_no_class(tag):
    return not tag.has_attr('class')

def get_html(driver):
	element = driver.wait.until(ec.presence_of_element_located((By.CLASS_NAME, "table__row")))
	html = driver.page_source
	return html


def get_content(html):
	soup = BeautifulSoup(html,'html.parser')
	matches = [] 
	flag = 0
	table = soup.find('table',class_='table')
	desks = table.find_all('tbody',class_='table__body')
	#print("Кря_desks:",len(desks))
	i = 1
	for desk in desks:
		#print("	Кря_desk_"+str(i))
		i = i+1
		comp = ""
		games = []
		rows = desk.find_all('tr',class_='table__row')
		#print("		Кря_rows:",len(rows))
		for row in rows:
			if row == rows[0]:
				headline = row.find("th")
				if headline != None:
					comp = headline.find("h2",class_='table__title-text').get_text(strip=True)
					#print('	Кря_comp: ' + comp)
			else:
				notmatch = row.find('td',class_='table-complex__wrap')
				notlive = row.find('div',class_='table__live')
				if (notmatch == None) and (notlive == None):
					flag = 1
					bothteams = row.find('h3',class_='table__match-title-text').get_text(strip=True)
					#print('		Кря: '+bothteams)
					team1 = bothteams[:bothteams.find(' — ')]
					team2 = bothteams[bothteams.find(' — ')+3:]
					#print('		Кря_teams: '+team1+' : '+team2)
					datetime = row.find('div',class_='table__timescore')					
					str_datetime = datetime.find(has_no_class).get_text(strip=True)
					str_date = str_datetime[:str_datetime.find(' в ')]
					date = format_date(str_date)
					str_time = str_datetime[str_datetime.find(' в ')+3:]
					time = format_time(str_time)
					coefs = row.find_all('td',class_='_type_btn',limit=3)
					try:
						c1 = float(coefs[0].get_text(strip=True))
						cX = float(coefs[1].get_text(strip=True))
						c2 = float(coefs[2].get_text(strip=True))
					except ValueError:
						pass
						#print('		Кря_game:',team1,'vs',team2,'|',str_date,str_time,'|','нет коэффициентов')
					else:
						#print('		Кря_game:',team1,'vs',team2,'|',str_date,str_time,'|',c1,'|',cX,'|',c2)
						games.append({
							'type':'game',
							'date':date,
							'time':time,
							'team1':team1,
							'team2':team1,
							'k1':c1,
							'kx':cX,
							'k2':c2
						})		
		if flag == 1:
			matches.append({'type':'comp','name':comp})
			matches.extend(games)

	return matches

def save_file(items,path):
	with open(path,'w',newline='') as file:
			writer = csv.writer(file,delimiter=';')
			for item in items:
				if item['type'] == 'comp':
					writer.writerow([item['name']])
					writer.writerow(['Дата','Время','Команда 1','Команда 2','1', 'Х', '2'])
				else:
					writer.writerow([item['date'],item['time'],item['team1'],item['team2'],str(item['k1']), str(item['kx']), str(item['k2'])])

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
		matches = get_content(html)
		save_file(matches,FILE)
	finally:
		#time.sleep(2)
		#print('Кря_совсем_конец')
		driver.quit()

def main():
	parse()

if __name__ == '__main__':
	main()