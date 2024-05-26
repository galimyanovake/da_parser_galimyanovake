from selenium import webdriver
from bs4 import BeautifulSoup
import time
from parse import parse
from sqlite import loadtosql, initializedb, test
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Edge()

url = "https://store.steampowered.com/search/?sort_by=filter=topsellers"

#for i in range(1, 6):
  #driver.get(f"{url}%page={i}")

#Так как там как таковый страниц нет и игры добавляются все ниже и ниже, программа прокручивает 5 раз вниз
driver.get(url)
for scroll in range(1, 10):
  driver.execute_script(f"window.scrollTo(0, {5000 * scroll})")
  time.sleep(1) 

driver.execute_script(f"window.scrollTo(0, 0)")
time.sleep(1)

try:
  element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "search_resultsRows"))
  )
finally:
  initializedb()
  loadtosql(parse(BeautifulSoup(driver.page_source, "lxml")))
driver.quit()
test()


    


