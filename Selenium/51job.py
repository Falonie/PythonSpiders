from selenium import webdriver
import requests
from lxml import html

# def phantomJS():
#     driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
#     driver.get('http://51job.com/')
#     driver.find_element_by_id("kwdselectid").send_keys('上海君果信息技术有限公司')
#     driver.find_element_by_xpath('//div[@class="ush top_wrap"]/button').click()
#     # print(driver.page_source)
#
# if __name__ == '__main__':
#     phantomJS()

with open('E:\company.txt','r') as f:
    for i, line in enumerate(f.readlines(), 1):
        line = line.strip()
        print(i, line)
        driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.get('http://51job.com/')
        driver.find_element_by_id("kwdselectid").send_keys(line)
        driver.find_element_by_xpath('//div[@class="ush top_wrap"]/button').click()
