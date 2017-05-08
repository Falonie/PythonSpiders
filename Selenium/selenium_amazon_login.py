from selenium import webdriver

#driver=webdriver.PhantomJS(executable_path='G:\phantomjs-2.1.1-windows\\bin\phantomjs.exe')
driver=webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
driver.get('https://www.amazon.cn/ap/signin?_encoding=UTF8&openid.assoc_handle=cnflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.cn%2Fref%3Dnav_signin%3Ftag%3Dzcn0e-23')
# driver.get('https://www.amazon.cn/ref=z_cn?tag=zcn0e-23')
email=driver.find_element_by_name('email')
email.send_keys('541002901@qq.com')
password=driver.find_element_by_id('ap_password')
password.send_keys('')  #enter password here
submit=driver.find_element_by_id('signInSubmit')
submit.click()

try:
    driver.find_element_by_id("dcq_question_subjective_1").send_keys('18221140594')
    driver.find_element_by_id("dcq_submit").click()
except Exception as e:
    driver.find_element_by_xpath('//select[@class="nav-search-dropdown searchSelect"]/option[@value="search-alias=stripbooks"]').click()
    driver.find_element_by_id('twotabsearchtextbox').send_keys('python')
    driver.find_element_by_class_name('nav-input').click()
else:
    driver.find_element_by_xpath('//select[@class="nav-search-dropdown searchSelect"]/option[@value="search-alias=stripbooks"]').click()
    driver.find_element_by_id('twotabsearchtextbox').send_keys('python')
    driver.find_element_by_class_name('nav-input').click()
    driver.find_element_by_id('pagnNextString').click()