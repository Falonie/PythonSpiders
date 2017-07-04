import parsel,time,csv,re
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# def scrape():
with open('E:\BOSS.txt','r') as f:
    for line in f.readlines():
        l = line.strip()
        driver = webdriver.PhantomJS(executable_path=r'E:\files\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        driver.get('https://www.zhipin.com/job_detail/?query=&scity=101020100&source=2')
        company = driver.find_element_by_name('query')
        company.clear()
        company.send_keys(l)
        driver.find_element_by_xpath('//form[@action="/job_detail/"]/button[@class="btn btn-search"]').click()
        # driver.find_element_by_xpath('//div[@class="info-primary"]/h3[@class="name"]').click()
        driver.find_element_by_xpath('//div[@class="info-primary"]/h3[@class="name"]').click()
        sel = parsel.Selector(text=driver.page_source)
        company = sel.xpath('//div[@class="info-primary"]/h3/text()').extract()
        recruit = sel.xpath('//div[@class="company-tab"]/a[2]/text()').extract()
        # print(company,recruit)
        for c, r in zip(company, recruit):
            print(c, r)

            with open('boss.csv', 'a+', newline='') as f2:
                writer = csv.writer(f2)
                writer.writerow((c, r))
        time.sleep(6)
    time.sleep(5)

# if __name__ == '__main__':
#     scrape()