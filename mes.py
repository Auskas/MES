#! /usr/bin/python3
# mes.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
import json
import logging

def get_random_time():
	return random.uniform(0.5, 2)

def get_random_time_slide():
	return random.uniform(20, 35)

def search_a_topic():
	try:
	    element = WebDriverWait(driver, 10).until(
	        EC.presence_of_element_located((By.CLASS_NAME, 'searchInput-86'))
	    )
	except Exception as exc:
		logger.error('Cannot find the search field.')
	finally:
		logger.debug('The search field has been found.')
	    #driver.quit()

	time.sleep(get_random_time())
	search_field = driver.find_element_by_class_name('searchInput-86')

	search_field.clear()
	time.sleep(get_random_time())

	search_field.send_keys(f'Музыка {random.choice(TOPICS)}')
	search_field.send_keys(Keys.RETURN)

	time.sleep(get_random_time())

def all_scenarios_checkbox():
	try:
	    element = WebDriverWait(driver, 10).until(
	        EC.presence_of_element_located((By.CLASS_NAME, 'checkbox-161'))
	    )
	except Exception as exc:
		logger.error('Cannot locate the lessons scenarios checkbox.')
	finally:
	    logger.debug('The lessons scenarios checkbox has been located.')

	logger.info('##################')
	logger.debug('Found scenarios checkbox.')
	time.sleep(get_random_time())
	#lesson = driver.find_element_by_class_name('checkbox-161')
	lesson = driver.find_elements_by_xpath("//*[contains(text(), 'Сценарии уроков')]")
	lesson = lesson[0]
	action.move_to_element(lesson)
	action.perform()
	logger.debug('Moved to the scenarios checkbox.')
	time.sleep(get_random_time())
	lesson.click()
	logger.debug('Clicked the scenarios checkbox.')
	time.sleep(get_random_time())

def random_scenario_choice():
	try:
	    element = WebDriverWait(driver, 10).until(
	        EC.presence_of_element_located((By.CLASS_NAME, 'materials-352'))
	    )
	except Exception as exc:
		logger.error('Cannot locate the scenarios.')
	finally:
	    logger.info('The scenarios have been located.')
	"""lesson = driver.find_elements_by_class_name('cardCover-289')
	lesson = lesson[random_lesson]
	driver.execute_script("arguments[0].scrollIntoView();", lesson)
	logger.info('scrollIntoView')
	time.sleep(1)
	logger.info('Moving to the element')
	logger.info('##################')"""
	time.sleep(get_random_time())
	lesson = driver.find_elements_by_xpath("//span[@class='title-65' and text()='Просмотреть']")
	random_lesson = random.randint(0,len(lesson) - 1)
	logger.info(f'Random lesson number {random_lesson + 1} has been chosen')
	logger.info(f'Number of lessons on the page: {len(lesson)}')
	lesson = lesson[random_lesson]
	driver.execute_script("arguments[0].scrollIntoView();", lesson)
	time.sleep(get_random_time())
	lesson.click()
	logger.debug('Clicked on the scenario.')
	time.sleep(get_random_time())

def scenario_walker():
	try:
	    element = WebDriverWait(driver, 10).until(
	        EC.presence_of_element_located((By.CLASS_NAME, 'lessonStageBookItem'))
	    )
	except Exception as exc:
		logger.error('Cannot locate the slides')
	finally:
	    logger.info('The slides have been located.')

	lesson = driver.find_elements_by_class_name('lessonStageBookItem')
	logger.info(f'Number of slides in the scenario: {len(lesson)}')
	for i in range(len(lesson)):
		print(f'Choosing slide number {i + 1}')
		driver.execute_script("arguments[0].scrollIntoView();", lesson[i])
		lesson[i].click()
		time.sleep(get_random_time_slide())
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(get_random_time_slide())

with open('topics.txt', 'r') as topics_file:
	TOPICS = json.load(topics_file)

if len(TOPICS) == 0:
	TOPICS = ['Математика 1 класс']

logger = logging.getLogger('MESH_RU')
logger.setLevel(logging.DEBUG)
logFileHandler = logging.FileHandler('tempal_log.txt')
logFileHandler.setLevel(logging.DEBUG)
logConsoleHandler = logging.StreamHandler()
logConsoleHandler.setLevel(logging.INFO)
formatterFile = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatterConsole = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
logFileHandler.setFormatter(formatterFile)
logConsoleHandler.setFormatter(formatterConsole)
logger.addHandler(logFileHandler)
logger.addHandler(logConsoleHandler)

logger.info('########## SCRIPT STARTED ##########')
driver = webdriver.Firefox()
driver.get("https://uchebnik.mos.ru/catalogue")
#driver.get("https://uchebnik.mos.ru/composer2/lesson/97265/view")
#driver.get("https://uchebnik.mos.ru/composer2/lesson/83730/view")
action = ActionChains(driver)
search_a_topic()
all_scenarios_checkbox()
random_scenario_choice()
time.sleep(2)
driver.switch_to.window(driver.window_handles[1])
time.sleep(get_random_time_slide())
scenario_walker()


