from selenium import webdriver
import time

def main():
    driver = webdriver.Chrome(executable_path='/media/salesmind/Work/chromedriver')
    # driver.maximize_window()
    driver.get('https://ehire.51job.com/')
    driver.find_element_by_xpath('//*[@id="txtMemberNameCN"]').send_keys('超乐健康')
    driver.find_element_by_xpath('//*[@id="txtUserNameCN"]').send_keys('超乐健康')
    driver.find_element_by_xpath('//div[@class="inpRegion"]/input[@name="txtPasswordCN"]').send_keys('salesmind1800')
    driver.find_element_by_xpath('//div[@class="inpList_bot"]/div/label').click()
    # driver.delete_all_cookies()
    time.sleep(20)
    driver.get('https://ehire.51job.com/Navigate.aspx?ShowTips=11&PwdComplexity=N')
    time.sleep(10)
    print(driver.get_cookies())

if __name__ == '__main__':
    main()