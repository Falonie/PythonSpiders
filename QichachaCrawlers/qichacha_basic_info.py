# -*- coding: utf-8 -*-
__author__ = 'Falonie'
import requests
import re
import pymongo
import time
import xlrd
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
cookies = {
    'Cookie': 'acw_tc=AQAAABgFeicdRw0Ao/ycy0O1A1zlaoSI; PHPSESSID=ccga6okdop91ge6b34054hb766; UM_distinctid=160fcf6271d506-0ba8b283e8d2a2-3a760e5d-100200-160fcf6271e416; zg_did=%7B%22did%22%3A%20%22160fcf6273736c-0f5f15548cac9f-3a760e5d-100200-160fcf627387e3%22%7D; _uab_collina=151607248499256448881892; _umdata=0712F33290AB8A6D7200D5AC434E5E0348CEA517391D874DCBE66267A34DEBCA17C85FDAA43E1B63CD43AD3E795C914C10C8ABF08DECF94385023B407D7D3633; hasShow=1; CNZZDATA1254842228=970305631-1516067880-%7C1516783216; acw_sc__=5a6854b9579cf38640edc6ea7da106d7cd5ac989; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516786876663%2C%22updated%22%3A%201516787282788%2C%22info%22%3A%201516696506138%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%228df61d213235daf577fa1bf530ea2748%22%7D'}
# connection = pymysql.connect(host='localhost', user='root', password='1234', db='employee', charset='utf8mb4')
collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie']['qichacha_basic_info_test']
session = requests.session()
file_path = '/media/salesmind/000CFFD8000DB949/Ctrip/壳牌-197-01.24.xlsx'


def company_list_excel(file_path):
    with xlrd.open_workbook(file_path) as data:
        table = data.sheets()[0]
        # print(table.ncols)
        for rownum in range(18, table.nrows):
            row = table.row_values(rownum)
            yield 'http://www.qichacha.com/search?key={}'.format(str(row[0]).strip())


def get_unique_key(url):
    response = session.get(url=url, headers=headers, cookies=cookies).text
    selector = html.fromstring(response)
    try:
        # company_name = selector.xpath('//*[@id="searchlist"]/table[1]/tbody/tr[1]/td[2]/a/em/em/text()|'
        #                               '//*[@id="searchlist"]/table[1]/tbody/tr[1]/td[2]/a/em/text()')[0]
        company_name = selector.xpath('//*[@id="searchlist"]/table/tbody/tr[1]/td[2]/a/descendant::text()')
        company_name = ''.join(str(i).strip() for i in company_name)
        href = selector.xpath('//*[@id="searchlist"]/table[1]/tbody/tr/td[2]/a/@href')[0]
        unique_key = re.split(r'[_.]', href)[1]
        email = selector.xpath('//*[@id="searchlist"]/table/tbody/tr[1]/td[2]/p[2]/span/text()')
        email = ''.join(str(i).strip() for i in email)
        legal_representative = selector.xpath('//*[@id="searchlist"]/table/tbody/tr[1]/td[2]/p[1]/a/text()')
        legal_representative = ''.join(str(i).strip() for i in legal_representative)
        telephone = selector.xpath('//*[@id="searchlist"]/table/tbody/tr[1]/td[2]/p[2]/text()')
        telephone = ''.join(str(i).strip() for i in telephone)
        # print(company_name, href, unique_key)
    except Exception as e:
        pass
    else:
        basic_url = 'http://www.qichacha.com/company_getinfos?unique={unique}&companyname={company}&tab=base'
        basic_url = basic_url.format(unique=unique_key, company=company_name)
        business_url = 'http://www.qichacha.com/company_getinfos?unique={0}&companyname={1}&tab=run'
        business_url = business_url.format(unique_key, company_name)
        time.sleep(4)
        # return basic_url, business_url
        item = {'company_name': company_name, 'telephone': telephone, 'email': email,
                'legal_representative': legal_representative}
        return item, basic_url, business_url


def parse_basic(url):
    item = {}
    r = session.get(url=url, headers=headers, cookies=cookies).text
    sel = html.fromstring(r)
    for _ in sel.xpath('//*[@id="Cominfo"]/table[2]/tr'):
        title = _.xpath('td[position()=1 or position()=3]/text()')
        info = _.xpath('td[position()=2 or position()=4]/text()')
        # print(title,info)
        item.update({str(t).strip().replace('：', ''): str(i).strip() for t, i in zip(title, info)})
        # for t,i in zip(title,info):
        #     print(str(t).strip(),str(i).strip())
    # print(item)
    for i, _ in enumerate(sel.xpath('//*[@id="Mainmember"]/table/tr[position()>1]'), 1):
        staff = _.xpath('td/text()|td/a/text()')
        c = 'staff{}'.format(i)
        d = ','.join(str(i).strip() for i in staff)
        # print({c:d})
        item[c] = d
    introduction = sel.xpath('//section[@id="Comintroduce"]/div[2]/div/descendant::text()')
    item['introduction'] = re.sub(r'[\n ]', '', ''.join(str(i).strip() for i in introduction))
    item['分支机构'] = sel.xpath('//*[@id="Subcom"]/div[1]/span[2]/text()')
    return item


def parse_business(url):
    r = session.get(url=url, headers=headers, cookies=cookies).text
    sel = html.fromstring(r)
    item2 = {}
    jobs_amout = sel.xpath('//section[@id="joblist"]/div[1]/span/text()')
    item2['jobs_amout'] = ''.join(str(i) for i in jobs_amout)
    job_release_lates_date = sel.xpath('//section[@id="joblist"]/table[@class="ntable ntable-odd"]/'
                                       'tbody/tr[2]/td/descendant::text()')
    item2['latest_job'] = ','.join(str(i).strip() for i in job_release_lates_date)
    for i in sel.xpath('//*[@id="V3_cwzl"]/table/tr'):
        title = i.xpath('td[position()=1 or position()=3]/text()')
        content = i.xpath('td[position()=2 or position()=4]/text()')
        item2.update({str(k).strip().replace('：', ''): str(v).strip() for k, v in zip(title, content)})
    for i in sel.xpath('//section[@id="financingList"]/table[@class="m_changeList"]'):
        head = i.xpath('thead/th/text()')
        item = i.xpath('tbody/tr[1]/td/descendant::text()')
        financing_content = [str(i).strip() for i in item]
        financing_content = list(filter(lambda x: len(x) > 1, financing_content))
        item2.update({k: v for k, v in zip(head, financing_content)})
    # print(item2)
    return item2


def manage():
    try:
        for url in company_list_excel(file_path):
            unique_key = get_unique_key(url)
            if unique_key:
                print(unique_key)
                _, basic_url, business_url = unique_key
                item = {**_, **parse_basic(basic_url), **parse_business(business_url)}
                print(item)
                collection.insert(item)
                time.sleep(15)
                continue
    except Exception as e:
        print(e)


if __name__ == '__main__':
    manage()