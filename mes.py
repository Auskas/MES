#! /usr/bin/python3
# mes.py - скрипт для автоматизации просмотра сценариев уроков Библиотеки МЭШ.
# Работает как в семействе Windows, так и Linux. Работоспособность в MacOS не проверялась.
# Используемый браузер Mozilla Firefox (необходим установленный geckodriver).
# Возможности: автоматический ввод логина и пароля (берутся из файла credentials.txt в директории скрипта);
#              автоматический выбор названия случайного сценария (список берётся из файла topics.txt);
#              автоматический перебор всех слайдов в сценарии со случайным временем просмотра;
#              автоматический запуск аудио атомиков на слайдах со случайным временем прослушивания;
#              отчёт о количестве просмотренных сценариев, слайдов, общего времени и т.п. за сессию.

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
import sys, os
import threading

def get_random_time():
	return random.uniform(0.5, 2)

def get_random_time_slide():
	return random.uniform(40, 65)

def get_random_number_of_scenarios():
	return random.randint(3,5)

def get_random_time_playback():
	return random.randint(30,180)

def login():
	try:
	    element = WebDriverWait(driver, 10).until(
	        #EC.presence_of_element_located((By.CLASS_NAME, 'loginButton-29'))
                EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'loginButton')]"))
	    )
	except Exception as exc:
		logger.error('Cannot find the login button.')
		driver.quit()
		sys.exit()
	finally:
		logger.debug('The login button has been found.')

	time.sleep(get_random_time())	
	login_button = driver.find_element_by_xpath("//span[contains(@class, 'loginButton')]")

	driver.execute_script("arguments[0].scrollIntoView();", login_button)
	logger.debug('Scrolling the login button into view...')
	time.sleep(get_random_time())
	action = ActionChains(driver)
	action.move_to_element(login_button)
	action.perform()
	time.sleep(get_random_time())

	login_button.click()

	try:
	    element = WebDriverWait(driver, 10).until(
	        EC.presence_of_element_located((By.ID, 'login-field'))
	    )
	except Exception as exc:
		logger.error('Cannot find the login field.')
		driver.quit()
		sys.exit()
	finally:
		logger.debug('The login field has been found.')
	login_field = driver.find_element_by_id('login-field')
	time.sleep(get_random_time())
	action = ActionChains(driver)
	action.move_to_element(login_field)
	action.perform()
	time.sleep(get_random_time())
	login_field.clear()
	login_field.send_keys(login_str)
	logger.info('Login has been entered into the login field.')

	password_field = driver.find_element_by_id('password-field')
	time.sleep(get_random_time())
	action = ActionChains(driver)
	action.move_to_element(password_field)
	action.perform()
	time.sleep(get_random_time())
	password_field.clear()
	password_field.send_keys(password_str)
	logger.info('Password has been entered into the password field.')	

	to_the_library = driver.find_element_by_xpath("//*[contains(text(), 'Войти в библиотеку')]")
	time.sleep(get_random_time())
	action = ActionChains(driver)
	action.move_to_element(to_the_library)
	action.perform()
	time.sleep(get_random_time())
	to_the_library.click()
	logger.info('Trying to log in...')
	time.sleep(get_random_time())
	time.sleep(get_random_time())
	time.sleep(get_random_time())
	try:
		to_the_library = driver.find_element_by_xpath("//*[contains(text(), 'Войти в библиотеку')]")
		logger.error(f'Cannot log in, probably wrong credentials.')
		driver.quit()
		sys.exit()
	except Exception as exc:
		logger.info('Successfully logged in!')

def search_a_topic():
	try:
	    element = WebDriverWait(driver, 10).until(
	        #EC.presence_of_element_located((By.CLASS_NAME, 'searchInput-86'))
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'searchInput')]"))
	    )
	except Exception as exc:
		logger.error('Cannot find the search field.')
		driver.quit()
		sys.exit()
	finally:
		logger.debug('The search field has been found.')

	time.sleep(get_random_time())
	search_field = driver.find_element_by_xpath("//input[contains(@class, 'searchInput')]")

	search_field.clear()
	time.sleep(get_random_time())

	search_topic = random.choice(TOPICS)
	names_of_scenarios_watched.append(search_topic)
	logger.info(f'Topic "{search_topic}" has been chosen.')

	search_field.send_keys(f'Музыка {search_topic}')
	search_field.send_keys(Keys.RETURN)

	time.sleep(get_random_time())

def all_scenarios_checkbox():
	try:
	    element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'checkbox')]"))
	    )
	except Exception as exc:
		logger.error('Cannot locate the lessons scenarios checkbox.')
		#driver.quit()
		#sys.exit()
	finally:
	    logger.debug('The lessons scenarios checkbox has been located.')

	time.sleep(get_random_time())
	lesson = driver.find_elements_by_xpath("//*[contains(text(), 'Сценарии уроков')]")
	lesson = lesson[0]
	action = ActionChains(driver)
	action.move_to_element(lesson)
	action.perform()
	logger.debug('Moved to the scenarios checkbox.')
	time.sleep(get_random_time())
	lesson.click()
	logger.debug('Clicked the scenarios checkbox.')
	time.sleep(get_random_time())

def random_scenario_choice():
	"""try:
	    element = WebDriverWait(driver, 10).until(
	        EC.presence_of_element_located((By.CLASS_NAME, 'material'))
	    )"""
	try:
	    element = WebDriverWait(driver, 10).until(
	        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'material')]"))
	    )
	except Exception as exc:
		logger.error(f'Cannot locate the scenarios: {exc}')
		#driver.quit()
		#sys.exit()
	finally:
	    logger.info('The scenarios have been located.')
	time.sleep(get_random_time())
	lesson = driver.find_elements_by_xpath("//span[@class='title-65' and text()='Просмотреть']")
	random_lesson = random.randint(0,len(lesson) - 1)
	logger.info(f'Random lesson number {random_lesson + 1} has been chosen')
	logger.info(f'Number of lessons on the page: {len(lesson)}')
	lesson = lesson[random_lesson]
	time.sleep(get_random_time())
	try:
		action = ActionChains(driver)
		action.move_to_element(lesson)
		action.perform()
		time.sleep(get_random_time())
		lesson.click()
		logger.debug('Clicked on the scenario.')
		time.sleep(get_random_time())
	except Exception as exc:
		logger.error(f'Cannot choose the scenario: {exc}')
		time.sleep(get_random_time())
		random_scenario_choice()                

def scenario_walker(total_number_of_slides_seen, total_number_of_audio_atomics_played):
	try:
	    element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'styles_stagePreview')]"))
	        #EC.presence_of_element_located((By.CLASS_NAME, 'lessonStageBookItem'))
	    )
	except Exception as exc:
		logger.error(f'Cannot locate the slides: {exc}')
	finally:
	    logger.info('The slides have been located.')

	#lesson = driver.find_elements_by_class_name('lessonStageBookItem')
	lesson = driver.find_elements_by_xpath("//div[contains(@class, 'styles_stagePreview')]")
	logger.info(f'Number of slides in the scenario: {len(lesson)}')
	time.sleep(get_random_time())
	for i in range(len(lesson)):
		print(f'Choosing slide number {i + 1}')
		driver.execute_script("arguments[0].scrollIntoView();", lesson[i])
		lesson[i].click()
		time.sleep(get_random_time_slide())
		audios = driver.find_elements_by_class_name('audioAtomic')
		print(f'Number of audio atomics in the slide: {len(audios)}')
		for j in range(len(audios)):
			try:
			    element = WebDriverWait(driver, 10).until(
			        EC.presence_of_element_located((By.CLASS_NAME, 'audioAtomic'))
			    )
			except Exception as exc:
				logger.error(f'Cannot locate the audio atomic: {exc}')
				continue
			finally:
			    logger.info('The audio atomic have been located.')

			try:
				action = ActionChains(driver)
				time.sleep(get_random_time())

				#driver.execute_script("arguments[0].scrollIntoView();", audios[j])
				#time.sleep(get_random_time())

				action.move_to_element(audios[j])
				action.perform()

				time.sleep(get_random_time())

				action.click()
				action.perform()

				time.sleep(get_random_time())
				playback_time = get_random_time_playback()
				logger.info(f'The random audio playback time is {playback_time} seconds.')

				action.send_keys(Keys.SPACE)
				action.perform()

				logger.info('The audio atomic is being played now.')
				time.sleep(playback_time)

				total_number_of_audio_atomics_played += 1
			except Exception as exc:
				logger.error(exc)
		total_number_of_slides_seen += 1
	return total_number_of_slides_seen, total_number_of_audio_atomics_played

with open('topics.txt', 'r') as topics_file:
	TOPICS = json.load(topics_file)

with open('credentials.txt', 'r') as credentials_file:
	login_str, password_str = credentials_file.readlines()

if len(TOPICS) == 0:
	TOPICS = ['Математика 1 класс']

logger = logging.getLogger('MESH_RU')
logger.setLevel(logging.DEBUG)
logFileHandler = logging.FileHandler('MES_logs.txt')
logFileHandler.setLevel(logging.DEBUG)
logConsoleHandler = logging.StreamHandler()
logConsoleHandler.setLevel(logging.INFO)
formatterFile = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatterConsole = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
logFileHandler.setFormatter(formatterFile)
logConsoleHandler.setFormatter(formatterConsole)
logger.addHandler(logFileHandler)
logger.addHandler(logConsoleHandler)

# Session counters: number of slides browsed, names of scenarios chosen etc.
total_number_of_slides_seen = 0
names_of_scenarios_watched = []
session_start_time = time.perf_counter()
total_number_of_audio_atomics_played = 0

logger.info('########## SCRIPT STARTED ##########')
if sys.platform == 'win32':
	os.chdir(f'G:{os.sep}PYTHON{os.sep}MES')
	driver = webdriver.Firefox()
else:
	driver = webdriver.Firefox()
main_window = driver.current_window_handle

driver.get("https://uchebnik.mos.ru/catalogue")
#driver.get("https://uchebnik.mos.ru/composer3/lesson/1483335/view")

# Calls a function that log into the service using personal credentials.
login()
# Calls a function that chooses 'all scenarios' filter in the main window.
all_scenarios_checkbox()
total_number_of_scenarios_to_walk = get_random_number_of_scenarios()
for i in range(total_number_of_scenarios_to_walk):
	logger.info(f'### Proceeding to the scenario {i+1} out of {total_number_of_scenarios_to_walk}###')
	# Calls a function that searches a random topic in the main window.
	search_a_topic()
	# Calls a function that chooses a random scenario on the page.
	random_scenario_choice()
	time.sleep(get_random_time())
	driver.switch_to.window(driver.window_handles[1])
	time.sleep(get_random_time())
	total_number_of_slides_seen, total_number_of_audio_atomics_played = scenario_walker(total_number_of_slides_seen, total_number_of_audio_atomics_played)
	# To close the current tab the following hotkeys are used: Ctrl + w.
	driver.close()
	driver.switch_to.window(main_window)

# The following chunk of code is for the results printing.
logger.info(f'Total number of scenarios browsed: {total_number_of_scenarios_to_walk}')
logger.info(f'The following scenarios were watched: {",".join(names_of_scenarios_watched)}')

logger.info(f'Total number of slides seen: {total_number_of_slides_seen}')
logger.info(f'Total number of audio atomics played: {total_number_of_audio_atomics_played}')

total_time_browsed = time.perf_counter() - session_start_time
hours = int(total_time_browsed // 3600)
minutes = int((total_time_browsed - hours * 3600) // 60)
seconds = int(total_time_browsed - hours * 3600 - minutes * 60)
logger.info(f'Total session time: {hours} hour(s), {minutes} minute(s), {seconds} second(s).') 
logger.info('########## SCRIPT ENDED ##########')
