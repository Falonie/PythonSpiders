import pymongo, time
from lxml import html
from selenium import webdriver

collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['instagram_urls']


def pagesource():
    # driver = webdriver.Chrome(executable_path='/media/salesmind/0002C1F9000B55A8/Linux Softwares/chromedriver')
    driver = webdriver.Chrome(executable_path='G:\Python files\chromedriver.exe')
    driver.get('https://www.instagram.com/ahmad_monk/')
    driver.maximize_window()
    # print(driver.page_source)
    # js = "var q=document.documentElement.scrollTop=100000"
    js = "window.scrollTo(0, document.body.scrollHeight);"
    driver.execute_script(js)
    driver.find_element_by_xpath('//article[@class="_mesn5"]/div/a').click()
    for i in range(0, 30):
        driver.execute_script(js)
        # driver.implicitly_wait(7)
        time.sleep(5)
    time.sleep(3)
    return driver.page_source


def crawl_images(text):
    selector = html.fromstring(text)
    image_url_list = []
    for _ in selector.xpath('//div[@class="_mck9w _gvoze _f2mse"]'):
        href = _.xpath('a/@href')[0]
        image_url = _.xpath('a/div[@class="_e3il2"]/div[@class="_4rbun"]/img/@src')[0]
        image_dict = {'image_url': image_url, 'page_link': 'https://www.instagram.com{}'.format(href)}
        image_url_list.append(image_dict)
    collection.insert_many(image_url_list)
    return image_url_list


if __name__ == '__main__':
    print(crawl_images(text=pagesource()))
    pass
