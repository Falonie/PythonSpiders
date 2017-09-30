from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver=webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.get('https://www.zhihu.com#signin')
name=driver.find_element_by_name('account')
name.send_keys('541002901@qq.com')
password=driver.find_element_by_name('password')
password.send_keys('')
submit=driver.find_element_by_tag_name('button')
submit.click()