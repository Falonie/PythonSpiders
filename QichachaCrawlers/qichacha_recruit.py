# -*- coding: utf-8 -*-
import requests
import re
import time
import pymongo
import logging
import xlrd
from lxml import html

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
cookie = {
    'Cookie': 'acw_tc=AQAAABgFeicdRw0Ao/ycy0O1A1zlaoSI; PHPSESSID=ccga6okdop91ge6b34054hb766; UM_distinctid=160fcf6271d506-0ba8b283e8d2a2-3a760e5d-100200-160fcf6271e416; zg_did=%7B%22did%22%3A%20%22160fcf6273736c-0f5f15548cac9f-3a760e5d-100200-160fcf627387e3%22%7D; _uab_collina=151607248499256448881892; CNZZDATA1254842228=970305631-1516067880-%7C1516758123; _umdata=0712F33290AB8A6D7200D5AC434E5E0348CEA517391D874DCBE66267A34DEBCA17C85FDAA43E1B63CD43AD3E795C914C10C8ABF08DECF94385023B407D7D3633; hasShow=1; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516759542045%2C%22updated%22%3A%201516759985479%2C%22info%22%3A%201516696506138%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%228df61d213235daf577fa1bf530ea2748%22%7D'}
# connection = pymysql.connect(host='localhost', user='root', password='1234', db='Falonie', charset='utf8mb4')
recruit_collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie']['壳牌-测试-01.24_recruit']
session = requests.session()
file_path = '/media/salesmind/000CFFD8000DB949/Ctrip/壳牌-测试-01.24.xlsx'


def company_list(file_path):
    with open(file_path, 'r') as f:
        for i, line in enumerate(f.readlines(), 1):
            # print(i,line.strip())
            yield 'http://www.qichacha.com/search?key={}'.format(line.strip())


def read_excel(file_path):
    with xlrd.open_workbook(file_path) as data:
        table = data.sheets()[0]
        # print(table.ncols)
        for rownum in range(0, table.nrows):
            row = table.row_values(rownum)
            yield 'http://www.qichacha.com/search?key={}'.format(str(row[0]).strip())


def get_unique_key(url):
    response = session.get(url=url, headers=header, cookies=cookie).text
    selector = html.fromstring(response)
    try:
        company_name = selector.xpath('//*[@id="searchlist"]/table[1]/tbody/tr[1]/td[2]/a/em/em/text()|'
                                      '//*[@id="searchlist"]/table[1]/tbody/tr[1]/td[2]/a/em/text()')[0]
        href = selector.xpath('//*[@id="searchlist"]/table[1]/tbody/tr/td[2]/a/@href')[0]
        unique_key = re.split(r'[_.]', href)[1]
        # print(company_name, href, unique_key)
    except Exception as e:
        pass
    else:
        base_url = 'http://www.qichacha.com/company_getinfos?unique={unique}&companyname={company}'
        time.sleep(5)
        return base_url.format(unique=unique_key, company=company_name) + '&p={page}&tab=run&box=job'


def recruit(url):
    page_num = 1
    base_url = url
    while True:
        position = []
        try:
            print('page {}'.format(page_num), base_url.format(page=page_num))
            r = session.get(url=base_url.format(page=page_num), headers=header, cookies=cookie)
            selector = html.fromstring(r.text)
            pattern = re.compile(r'companyname=(.*?)&')
            company = pattern.findall(base_url)[0]
            for i in selector.xpath('//table[@class="ntable ntable-odd"]/tbody/tr[position()>1]'):
                job = i.xpath('td/descendant::text()')
                b = ','.join(str(i).strip() for i in job)
                # print(company, b)
                logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S: %p',
                                    level=logging.DEBUG)
                logging.info(msg='{0},{1}'.format(company, b))
                # with connection.cursor() as cursor:
                #     sql = "INSERT INTO qichacha_recruit (company,recruit) VALUES ('{}','{}')"
                #     # sql = 'insert into qichacha_recruit (recruit) VALUES (%s)'
                #     cursor.execute(query=sql.format(company, b))
                #     # cursor.execute(sql,(b))
                #     connection.commit()
                recruit_joblist = {'company': company, 'recruit_joblist': b}
                position.append(recruit_joblist)
            recruit_collection.insert_many(position)
            page_num += 1
            time.sleep(7)
        except Exception as e:
            break
        finally:
            time.sleep(5)


def manage():
    for i in read_excel(file_path):
        print(get_unique_key(url=i))
        recruit(url=get_unique_key(url=i))
        time.sleep(5)


if __name__ == '__main__':
    manage()