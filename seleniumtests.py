from concurrent.futures import thread
import sys
from threading import Thread
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def run_detectives(game_id: str, number: int):
    driver = webdriver.Chrome(sys.argv[1])
    driver.get(f"http://localhost:8000/{game_id}")
    assert "Scotland Yard" in driver.title
    elem = driver.find_element_by_id("player_name")
    elem.send_keys(f"d{number}")
    elem.send_keys(Keys.RETURN)
    sleep(10000)
    driver.close()


driver = webdriver.Chrome(sys.argv[1])
driver.get(f"http://localhost:8000/")
assert "Scotland Yard" in driver.title
elem = driver.find_element_by_id("player_name")
elem.send_keys("x")
elem.send_keys(Keys.RETURN)
sleep(1.1)
GAME_ID = driver.execute_script("return GAME_ID")

for i in range(1, 6):
    t = Thread(target=run_detectives, args=(GAME_ID, i),daemon=True)
    t.start() 

while driver.execute_script(
    "return document.getElementById('start').style.display !== 'initial';"
):
    sleep(0.5)
elem = driver.find_element_by_id("start")
elem.click()
while True:
    sleep(1)
driver.close()
