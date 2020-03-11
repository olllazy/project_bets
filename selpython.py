from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import sys
import csv


URL_LIGASTAVOK = 'https://www.ligastavok.ru/bets/my-line/soccer/rossiia-id-350'
HEADERS = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.136 YaBrowser/20.2.3.236 Yowser/2.5 Safari/537.36', 'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'} 
FILE_LIGASTAVOK = 'ligastavok/premyerliga.csv'

#def get_html(url,params=None):
# 	r = requests.get(url,headers=HEADERS,params=params)
#	return r

def get_content_ligastavok(driver):
	soup = BeautifulSoup(driver.page_source,'html.parser')
	desks = soup.find_all('div',class_='events-proposed__wrapper-events-f8fbd6')

	desk = desks[0] #Российская Премьер-Лига
	items = desk.find_all('div', class_='bui-event-row-9eed4e')
	itteams = desk.find_all('span',class_='bui-commands__command-251fef')
	teams = []
	for team in itteams:
		teams.append(team.get_text(strip=True))	
	
	itcoef = desk.find_all('div',class_='bui-outcome-4ce98d')
	#print(itcoef)
	coefs = []
	for coef in itcoef:
		coefs.append(coef.get_text(strip=True))	
	#print(coefs)
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
	return matches

def save_file_ligastavok(items,path):
	with open(path,'w',newline='') as file:
			writer = csv.writer(file,delimiter=';')
			writer.writerow(['Дата','Время','Команда 1','Команда 2','1', 'Х', '2'])
			for item in items:
				writer.writerow([item['date'],item['time'],item['team1'],item['team2'],item['k1'], item['kx'], item['k2']])

def parse_ligastavok(driver):
	#html = get_html(URL)
	#if html.status_code == 200:
	
	driver.get(URL_LIGASTAVOK) #,headers=HEADERS,params=params
	btn_elem = driver.find_elements_by_class_name("bui-events-lazy-bar__button-106539")
	for btn in btn_elem:
		driver.execute_script("document.querySelector('.bui-events-lazy-bar__button-106539').click();")
	matches = get_content_ligastavok(driver)
	#print(matches)
	save_file_ligastavok(matches,FILE_LIGASTAVOK)
	#else:
	#	print('Error')



def main():
	options = Options()
	options.add_argument('start-maximized')
	options.add_argument('disable-infobars')
#	chrome_options = webdriver.ChromeOptions()
#	chrome_options.add_argument("–disable-infobars")
#	chrome_options.add_argument("–enable-automation")
#	chrome_options.add_argument("–start-maximized")
#	chrome_options.add_argument("--disable-notifications")
	driver = webdriver.Chrome(chrome_options=options)

	parse_ligastavok(driver)
	#t = input("Введите число: ")
	driver.close()


#	while 1:
#		try:
#			btn_elem = driver.find_element_by_class_name("bui-events-lazy-bar__button-106539")
#			btn_elem.click()
#			
#		except:
#			break
	
#	script = “var callback = arguments[arguments.length - 1]; ” 
#	“window.setTimeout(function(){ callback(‘timeout’) }, 3000);” 
#	driver.execute_async_script(script)
						
	


if __name__ == "__main__": # если нужно будет подключить qparser
	main()