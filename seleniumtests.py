import imp
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from threading import Thread
from time import sleep

GAME_ID = None


def run_detectives(game_id: str, number: int):
    driver = webdriver.Chrome("C:\\dev\\Util\\chromedriver\\chromedriver.exe")
    driver.get(f"http://localhost:8000/{game_id}")
    assert "Scotland Yard" in driver.title
    elem = driver.find_element_by_id("player_name")
    elem.send_keys(f"d{number}")
    elem.send_keys(Keys.RETURN)
    # driver.close()
    sleep(10000)


def run_mr_x():
    global GAME_ID
    driver = webdriver.Chrome("C:\\dev\\Util\\chromedriver\\chromedriver.exe")
    driver.get(f"http://localhost:8000/")
    assert "Scotland Yard" in driver.title
    elem = driver.find_element_by_id("player_name")
    elem.send_keys("x")
    elem.send_keys(Keys.RETURN)
    GAME_ID = driver.execute_script("return GAME_ID;")
    sleep(15)
    elem = driver.find_element_by_id("start")
    elem.click()
    sleep(5)
    player_id = driver.execute_script("return PLAYER_ID;")
    elem = driver.find_element_by_id("ws-command")
    elem.send_keys(f"REQMOVE {player_id} taxi ")
    # driver.close()
    sleep(10000)


mr_x_thread = Thread(target=run_mr_x)
mr_x_thread.start()
# mr_x_thread.join()
sleep(10)
print(GAME_ID)
detective_threads = [
    Thread(target=run_detectives, args=(GAME_ID, i)) for i in range(1, 6)]
for thread in detective_threads:
    thread.start()
    # thread.join()