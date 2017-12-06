import requests, re, time, pymongo, pymysql, csv, logging, xlrd
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
cookies = {
    'Cookie': 'acw_tc=AQAAAI2uBjhmRQQAoPycy5C1aqwkvj9N; UM_distinctid=15e939f16eda87-07dc992df33a62-3976045e-13c680-15e939f16eee13; _uab_collina=150571523129578213034327; _umdata=A502B1276E6D5FEF52D1CA8DB60A65FF56B7E46B117EB5BABDBE67BF25441DBD9D7A0425DE027D29CD43AD3E795C914C0FF0994FB4B615CF34D62FAA808BADEE; PHPSESSID=j20g3kunfl4tuf1ori5jkgj5f5; hasShow=1; zg_did=%7B%22did%22%3A%20%2215e939f15579a1-09b9351d2370ab-3976045e-13c680-15e939f1558c20%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201505715230043%2C%22updated%22%3A%201505715462034%2C%22info%22%3A%201505715230046%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22c11b6f0a73cca35a27a8af6db3c88b92%22%7D; CNZZDATA1254842228=731759014-1505713978-%7C1505713978'}
connection = pymysql.connect(host='localhost', user='root', password='1234', db='Falonie', charset='utf8mb4')
shareholders_collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie']['qichacha_shareholders2']
session = requests.session()
file = '/media/salesmind/Other/云鸟-21.xlsx'


def company_list(file):
    with open(file, 'r') as f:
        for i, line in enumerate(f.readlines(), 1):
            # print(i,line.strip())
            yield 'http://www.qichacha.com/search?key={}'.format(line.strip())


def company_list_excel(file):
    with xlrd.open_workbook(file) as data:
        table = data.sheets()[0]
        # print(table.ncols)
        for rownum in range(0, table.nrows):
            row = table.row_values(rownum)
            yield 'http://www.qichacha.com/search?key={}'.format(str(row[0]).strip())


def get_unique_key(url):
    response = session.get(url=url, headers=headers, cookies=cookies).text
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
        base_url = 'http://www.qichacha.com/company_getinfos?unique={unique}&companyname={company}&tab=base'
        time.sleep(4)
        return base_url.format(unique=unique_key, company=company_name)


def shareholders(url):
    response = session.get(url=url, headers=headers, cookies=cookies).text
    sel = html.fromstring(response)
    pattern = re.compile(r'companyname=(.*?)&')
    company = pattern.findall(url)[0]
    shareholders_list = []
    try:
        for j, i in enumerate(sel.xpath('//*[@id="Sockinfo"]/table[@class="m_changeList"]/tr[position()>1]'), 1):
            s = i.xpath('td/text()|td/div/a[1]/text()')
            shareholder = ','.join(str(i).strip() for i in s)
            logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S: %p', level=logging.DEBUG)
            logging.info(msg='{} {}'.format(company, shareholder))
            # print(company, shareholder)
            shareholder_list = {'company': company, 'shareholder': shareholder}
            shareholders_list.append(shareholder_list)
        shareholders_collection.insert_many(shareholders_list)
        time.sleep(8)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    for i in company_list_excel(file):
        print(get_unique_key(url=i))
        shareholders(get_unique_key(i))
        # print(i)
        # print(get_unique_key(i))