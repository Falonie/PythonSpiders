from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver=webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.get('https://www.python.org/')
try:
    element=WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"id-search-field")))
finally:
    pass