import requests, time, csv, pymongo, xlrd
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie']['zdao_总经理']
file = '早稻采集字段_.xlsx'
file2 = 'Book2.xlsx'


class Obtain_urls(object):
    def generate_pagesource(self,path=None):
        # driver = webdriver.Chrome(executable_path='/media/salesmind/Other/Softwares/Linux softwares/chromedriver')
        driver = webdriver.Chrome(executable_path='G:\Python files\chromedriver.exe')
        driver.get('https://www.zdao.com/user/login?redirect=https%3A%2F%2Fwww.zdao.com%2F')
        driver.maximize_window()
        driver.find_element_by_xpath('//div[@data-stat-key="login_by_account"]').click()
        # driver.find_element_by_xpath('//div[@class="login_icon login_by_cc"]').click()
        # driver.find_element_by_xpath('//div[@class="login_icon login_by_cc"]/i').click()
        # js = "var q=document.documentElement.scrollTop=10"
        # driver.execute_script(js)
        # driver.find_element_by_id("input_phone").send_keys('15527510501')
        driver.find_element_by_xpath('//div[@class="login_by_account"]/div[1]/input[@class="input_text account"]').send_keys('15527510501')
        # driver.find_element_by_class_name("input_text").send_keys('15527510501')
        driver.find_element_by_xpath('//div[@class="login_by_account"]/div[2]/input[@class="input_text password"]').send_keys('salesmind2017')
        # driver.find_element_by_class_name("input_text password").send_keys('salesmind2017')
        driver.find_element_by_xpath('//div[@class="login_by_account"]/div[4]').click()
        # driver.find_element_by_id("account").send_keys('15527510501')
        # driver.find_element_by_id('password').send_keys('salesmind2017')
        # driver.find_element_by_id("btn_login").click()
        # driver.find_element_by_xpath('//li[@class="search_tab search_person"]').click()
        # driver.find_element_by_class_name("search_tab search_person").click()
        time.sleep(5)
        driver.find_element_by_xpath('//div[@class="search_box"]/ul/li[2]').click()
        driver.find_element_by_xpath('//input[@class="search_input"]').send_keys('总经理')
        driver.find_element_by_id('btn_search').click()
        time.sleep(2)
        # driver.find_element_by_xpath('//div[@class="filter_inner"]/i').click()
        # driver.find_element_by_xpath('//div[@data-name="北京"]/span').click()
        with xlrd.open_workbook(file) as data_:
            table = data_.sheets()[1]
            for rownum in range(48, table.nrows):
                row = table.row_values(rownum)
                driver.find_element_by_xpath('//div[@class="filter_inner"]/i').click()
                self.row_0 = row[0]
                self.row_1 = row[1]
                driver.find_element_by_xpath('//div[@data-name="{}"]/span'.format(self.row_0)).click()
                # driver.find_element_by_xpath('//div[@data-name="{}"]/span'.format(self.row_1)).click()
                time.sleep(5)
                # print(driver.page_source)
                while True:
                    yield driver.page_source
                    time.sleep(5)
                    js = "var q=document.documentElement.scrollTop=100000"
                    driver.execute_script(js)
                    try:
                        driver.find_element_by_xpath('//div[@class="sg_next_page sg_page_item icon_chevron_right"]').click()
                        time.sleep(3)
                    except Exception:
                        js2 = "var q=document.documentElement.scrollTop=1"
                        driver.execute_script(js2)
                        break
                # element = driver.find_element_by_xpath('//div[@class="filter_inner"]/i')
                # driver.execute_script("return arguments[0].scrollIntoView(true);", element)
                # continue
    def generate_pagesource_nmae_card(self,path=None):
        # driver = webdriver.Chrome(executable_path='/media/salesmind/Other/Softwares/Linux softwares/chromedriver')
        driver = webdriver.Chrome(executable_path='G:\Python files\chromedriver.exe')
        driver.get('https://www.zdao.com/user/login?redirect=https%3A%2F%2Fwww.zdao.com%2F')
        driver.maximize_window()
        driver.find_element_by_xpath('//div[@data-stat-key="login_by_account"]').click()
        driver.find_element_by_xpath('//div[@class="login_icon login_by_cc"]').click()
        # driver.find_element_by_xpath('//div[@class="login_icon login_by_cc"]/i').click()
        driver.find_element_by_id("account").send_keys('15527510501')
        driver.find_element_by_id('password').send_keys('salesmind2017')
        driver.find_element_by_id("btn_login").click()
        # driver.find_element_by_xpath('//li[@class="search_tab search_person"]').click()
        # driver.find_element_by_class_name("search_tab search_person").click()
        time.sleep(5)
        driver.find_element_by_xpath('//div[@class="search_box"]/ul/li[2]').click()
        driver.find_element_by_xpath('//input[@class="search_input"]').send_keys('CEO')
        driver.find_element_by_id('btn_search').click()
        time.sleep(2)
        # driver.find_element_by_xpath('//div[@class="filter_inner"]/i').click()
        # driver.find_element_by_xpath('//div[@data-name="北京"]/span').click()
        with xlrd.open_workbook(file) as data_:
            table = data_.sheets()[1]
            for rownum in range(1, table.nrows):
                row = table.row_values(rownum)
                driver.find_element_by_xpath('//div[@class="filter_inner"]/i').click()
                self.row_0 = row[0]
                self.row_1 = row[1]
                driver.find_element_by_xpath('//div[@data-name="{}"]/span'.format(self.row_0)).click()
                driver.find_element_by_xpath('//div[@data-name="{}"]/span'.format(self.row_1)).click()
                time.sleep(5)
                # print(driver.page_source)
                while True:
                    yield driver.page_source
                    time.sleep(5)
                    js = "var q=document.documentElement.scrollTop=100000"
                    driver.execute_script(js)
                    try:
                        driver.find_element_by_xpath('//div[@class="sg_next_page sg_page_item icon_chevron_right"]').click()
                        time.sleep(3)
                    except Exception:
                        js2 = "var q=document.documentElement.scrollTop=1"
                        driver.execute_script(js2)
                        break
                # element = driver.find_element_by_xpath('//div[@class="filter_inner"]/i')
                # driver.execute_script("return arguments[0].scrollIntoView(true);", element)
                # continue

    def generate_pagesource_(self):
        driver = webdriver.Chrome(executable_path='/media/salesmind/Other/Softwares/chromedriver')
        driver.get('https://www.zdao.com/user/login?redirect=https%3A%2F%2Fwww.zdao.com%2F')
        driver.find_element_by_xpath('//div[@data-stat-key="login_by_account"]').click()
        driver.find_element_by_xpath('//div[@class="login_icon login_by_cc"]').click()
        # driver.find_element_by_xpath('//div[@class="login_icon login_by_cc"]/i').click()
        driver.find_element_by_id("account").send_keys('17621063129')
        driver.find_element_by_id('password').send_keys('salesmind')
        driver.find_element_by_id("btn_login").click()
        # driver.find_element_by_xpath('//li[@class="search_tab search_person"]').click()
        # driver.find_element_by_class_name("search_tab search_person").click()
        time.sleep(5)
        driver.find_element_by_xpath('//div[@class="search_box"]/ul/li[2]').click()
        driver.find_element_by_xpath('//input[@class="search_input"]').send_keys('创始人')
        driver.find_element_by_id('btn_search').click()
        time.sleep(2)
        driver.find_element_by_xpath('//div[@class="filter_inner"]/i').click()
        # driver.find_element_by_xpath('//div[@data-name="北京"]/span').click()
        # driver.find_element_by_xpath('//div[@data-name="浙江"]/span').click()
        driver.find_element_by_xpath('//div[@data-name="宁波"]/span').click()
        # driver.find_element_by_xpath('//div[@data-name="杭州"]/span').click()
        time.sleep(5)
        # print(driver.page_source)
        while True:
            yield driver.page_source
            time.sleep(5)
            js = "var q=document.documentElement.scrollTop=100000"
            driver.execute_script(js)
            try:
                driver.find_element_by_xpath('//div[@class="sg_next_page sg_page_item icon_chevron_right"]').click()
                time.sleep(3)
            except Exception:
                break

    def get_urls(self, text):
        selector = html.fromstring(text)
        urls = selector.xpath('//a[@class="vp_name_link"]/@href')
        urls_list = ['https://www.zdao.com{}'.format(i) for i in urls]
        urls = [{'url': _, 'province': self.row_0, 'city': self.row_1} for _ in urls_list]
        return urls


def main():
    obtain_urls = Obtain_urls()
    for _ in obtain_urls.generate_pagesource():
        u = obtain_urls.get_urls(text=_)
        print(u)
        try:
            collection.insert_many(u)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()