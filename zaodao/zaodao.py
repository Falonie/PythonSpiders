import requests, pymongo, csv, time, re, xlrd
from lxml import html
# import pandas as pd

url = 'https://www.zdao.com/account/main?id=dcc902ad7c83bc0c855ddf5c463e377c&utype=0'
cookie = {
    'Cookie': 'JSESSID=juprtnreq00ardk5gsvft00al6; _cpcl=5a375ff51da7e; S2=803419491E4144BFhy67R7SC; Hm_lvt_dd717aa780606579d5c95d7bf64d529c=1513532216; Hm_lpvt_dd717aa780606579d5c95d7bf64d529c=1513532226'}
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
db = pymongo.MongoClient(host='localhost', port=27017)['Falonie']
# collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie']['zaodao']
file = 'zdao_法人_filter_duplicates.csv'
file2 = 'zdao_董事_filter_duplicates.xlsx'


class Zaodao(object):
    def read_csv(self, file):
        with open(file, 'r') as f:
            reader = csv.reader(f)
            for i, j in enumerate(reader, 1):
                # print(j[0], j[1])
                yield j

    def read_excel(self, file):
        with xlrd.open_workbook(file) as data_:
            table = data_.sheets()[0]
            for rownum in range(5374, table.nrows):
                self.row = table.row_values(rownum)
                yield self.row[0]

    def read_mongodb(self):
        collection = db['zdao_法人_filter_duplicates']
        for i, j in enumerate(collection.find({}), 1):
            # yield i,j['province'],j['city'],'https://' +j['url']
            yield j

    def parse(self, url):
        # url='https://www.zdao.com/site/searchperson?keywords=%E5%88%9B%E5%A7%8B%E4%BA%BA'
        r = requests.get(url=url, headers=header, cookies=cookie).text
        selector = html.fromstring(r)
        # href_list=selector.xpath('//div[@class="person_card "]/div[@class="vp_left "]/div[1]/a/@href')
        # href_list=selector.xpath('//a[@class="vp_img_wrapper"]/@href')
        # href=selector.xpath('//*[@id="person_list"]/div[2]/div[5]/div[1]/div[1]/a/@href')
        return r

    def parse_page_details(self, url):
        r = requests.get(url=url, headers=header, cookies=cookie).text
        selector = html.fromstring(r)
        collection = db['zdao_董事_filter_duplicates_crawled_result']
        for _ in selector.xpath('//div[@class="user_career"]'):
            user_name = ''.join(str(i).strip() for i in _.xpath('p[@class="user_name"]/text()'))
            user_title = ''.join(str(i).strip() for i in _.xpath('p[@class="user_title"]/text()'))
            user_company = ''.join(str(i).strip() for i in _.xpath('a[@class="user_company"]/text()'))
            business = ''.join(str(i).strip() for i in _.xpath('p[@class="business"]/text()'))
            # email=selector.xpath('')
            # print(user_name,user_title,user_company,business)
            # for _ in selector.xpath('//a[@data-stat-key="my_company_info"]'):
            small_title = ''.join(str(i).strip() for i in
                                  selector.xpath(
                                      '//a[@data-stat-key="my_company_info"]/div[@class="small_title"]/text()'))
            establish_time = ''.join(
                str(i).strip() for i in selector.xpath('//a[@data-stat-key="my_company_info"]/div[3]/text()'))
            establish_time = re.sub(r'[\xa0\t ]', '', establish_time)
            # print(small_title,establish_time)
            # ''.join(str(i).strip() for i in )
            # for _ in selector.xpath('//div[@class="half_item border_bottom"]'):
            eduction = ''.join(str(i).strip() for i in selector.xpath(
                '//div[@class="half_item border_bottom"]/div[@class="small_title"]/div/text()'))
            faculty = ''.join(str(i).strip() for i in selector.xpath(
                '//div[@class="half_item border_bottom"]/div[@class="half_item_info_wrapper"]/div/text()'))
            eduction_time = ''.join(str(i).strip() for i in selector.xpath(
                '//div[@class="half_item border_bottom"]/div[@class="half_item_info education_time"]/text()'))
            mobile = selector.xpath('//*[@class="item_info mobile_item"]/text()')
            mobile = ''.join(str(i).strip() for i in mobile)
            email = ''.join(
                str(i).strip() for i in selector.xpath('//a[@class="item_info mail_item contact_item"]/text()'))
            qq = ''.join(
                str(i).strip() for i in selector.xpath('//div[@class="item_info QQ_item contact_item"]/text()'))
            weixin = ''.join(
                str(i).strip() for i in selector.xpath('//div[@class="item_info weixin_item contact_item"]/text()'))
            gender = ''.join(str(i).strip() for i in selector.xpath('//div[@class="item_info gender"]/text()'))
            industry = ''.join(str(i).strip() for i in selector.xpath('//div[@class="item_info industry_name"]/text()'))
            location = ''.join(str(i).strip() for i in selector.xpath('//div[@class="item_info town_code"]/text()'))
            user = {'user_name': user_name, 'user_title': user_title, 'user_company': user_company,
                    'business': business,
                    'small_title': small_title, 'establish_time': establish_time, 'eduction': eduction,
                    'faculty': faculty,
                    'eduction_time': eduction_time, 'mobile': mobile, 'email': email, 'qq': qq, 'weixin': weixin,
                    'industry': industry, 'location': location,'url':self.row[0]}
            collection.insert_one(user)
            return user


def main_csv():
    zaodao = Zaodao()
    for i, j in enumerate(zaodao.read_csv(file), 1):
        print(i, j[0])
        print(zaodao.parse_page_details(url=j[0]))
        time.sleep(10)


def main_excel(file):
    zaodao = Zaodao()
    for i, j in enumerate(zaodao.read_excel(file), 1):
        print(i, j)
        print(zaodao.parse_page_details(url=j))
        time.sleep(15)


def main_mongodb():
    zaodao = Zaodao()
    for i, _ in enumerate(zaodao.read_mongodb(), 1):
        url = 'https://' + _['url'] if not str(_['url']).startswith('https://') else _['url']
        print(i, url)
        print(zaodao.parse_page_details(url=url))
        time.sleep(15)


if __name__ == '__main__':
    main_excel(file2)
    # main_mongodb()
    # main_csv()
    # zaodao = Zaodao()
    # for i, j in enumerate(zaodao.read_excel(file2), 1):
    #     print(i, j)