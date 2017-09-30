from selenium import webdriver

driver=webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.get('https://passport.36kr.com/pages/?ok_url=https%3A%2F%2F36kr.com%2F#/login?pos=header')
driver.find_element_by_id('kr-shield-username').clear()
driver.find_element_by_id('kr-shield-username').send_keys('18516630543')
driver.find_element_by_id('kr-shield-password').clear()
driver.find_element_by_id('kr-shield-password').send_keys('413154831')
# driver.find_element_by_xpath('//div[@class="form-group"]/input[@id="kr-shield-username"]').clear()
# driver.find_element_by_xpath('//div[@class="form-group"]/input[@id="kr-shield-username"]').send_keys('18516630543')
# driver.find_element_by_xpath('//div[@class="form-group"]/input[@name="password"]').clear()
# driver.find_element_by_xpath('//div[@class="form-group"]/input[@name="password"]').send_keys('413154831')
driver.find_element_by_id('kr-shield-submit').click()