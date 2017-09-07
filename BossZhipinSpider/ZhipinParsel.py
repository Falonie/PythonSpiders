import parsel, time, csv, re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# def scrape():
with open('E:\BOSS.txt', 'r') as f:
    # driver = webdriver.PhantomJS(executable_path=r'E:\files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    # driver.get('https://www.zhipin.com/job_detail/?query=&scity=101020100&source=2')
    for line in f.readlines():
        try:
            driver = webdriver.PhantomJS(executable_path=r'E:\files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
            # driver = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
            driver.get('https://www.zhipin.com/job_detail/?query=&scity=101020100&source=2')
            wait = WebDriverWait(driver, 10)
            l = line.strip()
            # company = driver.find_element_by_name('query')
            # submit = driver.find_element_by_xpath('//form[@action="/job_detail/"]/button[@class="btn btn-search"]')
            company = wait.until(EC.presence_of_element_located((By.NAME, 'query')))
            submit = wait.until(EC.presence_of_element_located((By.XPATH, '//form[@action="/job_detail/"]/button[@class="btn btn-search"]')))
            company.clear()
            company.send_keys(l)
            submit.click()
            # driver.find_element_by_xpath('//div[@class="info-primary"]/h3[@class="name"]').click()
            # submit2 = driver.find_element_by_xpath('//div[@class="info-primary"]/h3[@class="name"]')
            submit2 = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="info-primary"]/h3[@class="name"]')))
            submit2.click()
            sel = parsel.Selector(text=driver.page_source)
            company2 = sel.xpath('//div[@class="info-primary"]/h3/text()').extract()
            recruit = sel.xpath('//div[@class="company-tab"]/a[2]/text()').extract()
            # print(copany,recruit)
            for c, r in zip(company2, recruit):
                print(c, r)

                # with open('boss.csv', 'a+', newline='') as f2:
                #     writer = csv.writer(f2)
                #     writer.writerow((c, r))
        except Exception as e:
            pass
        time.sleep(6)
    time.sleep(5)

# if __name__ == '__main__':
#     scrape()