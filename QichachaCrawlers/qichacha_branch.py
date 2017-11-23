import requests, re, pymongo, time, xlrd, logging
from lxml import html

url = 'http://www.qichacha.com/company_getinfos?unique=518ef3a4b4a0ae4e6a58f8d288bdfd28&companyname=%E5%8C%97%E4%BA%AC%E7%A5%9E%E5%B7%9E%E6%95%B0%E7%A0%81%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&tab=base'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
cookies = {
    'Cookie': 'acw_tc=AQAAAKTc8GK7EgAAo/ycyzFO2mbih7Gu; UM_distinctid=15fc3be7c53a5-0a92c0bf8f304a-112b1709-13c680-15fc3be7c5424a; _uab_collina=151081756327655449988871; _umdata=65F7F3A2F63DF020F26352CB2D723F6947983530C33A3C5B703E522C5AAB7C1CA01A32ABB7CA0ECBCD43AD3E795C914C2053C5B223499DBB947E148B2D5581AE; PHPSESSID=njrm2b2gquobfttkbkbvsu7eh1; hasShow=1; zg_did=%7B%22did%22%3A%20%2215fc3be7c733af-0df765ef22e6ad-112b1709-13c680-15fc3be7c74463%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201511140268970%2C%22updated%22%3A%201511140343209%2C%22info%22%3A%201510817561724%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%228df61d213235daf577fa1bf530ea2748%22%7D; CNZZDATA1254842228=1519393824-1510815399-%7C1511136078'}
collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['branch']
file = '/media/salesmind/Other/cloud_bird/test_company.xlsx'
# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S: %p', level=logging.DEBUG)

# def company_list():
#     with open('/media/salesmind/Other/cloud_bird/云鸟-样本（招聘信息）.txt', 'r') as f:
#         for i, line in enumerate(f.readlines(), 1):
#             # print(i,line.strip())
#             yield 'http://www.qichacha.com/search?key={}'.format(line.strip())

def company_list(file):
    with xlrd.open_workbook(file) as data:
        table = data.sheets()[0]
        for rownum in range(1, table.nrows):
            row = table.row_values(rownum)
            yield 'http://www.qichacha.com/search?key={}'.format(str(row[0]).strip())


def get_unique_key(url):
    session = requests.session()
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
        time.sleep(5)
        return base_url.format(unique=unique_key, company=company_name)


def branch(url):
    try:
        response = requests.get(url=url, headers=headers, cookies=cookies).text
        sel = html.fromstring(response)
        pattern = re.compile(r'companyname=(.*?)&')
        company = pattern.findall(url)[0]
        branch_amount = sel.xpath('//*[@id="Subcom"]/div[1]/span[2]/text()')
        branch_amount = ''.join(str(i).strip() for i in branch_amount)
        branch_list = []
        for i in sel.xpath('//section[@id="Subcom"]/div[@id="V3_Subcom"]/ul/li'):
            branch_name = i.xpath('descendant::text()')
            branch_name = ''.join(str(i).strip() for i in branch_name)
            print(company, branch_name, branch_amount)
            logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S: %p', level=logging.DEBUG)
            logging.info(msg='{0},{1},{2}'.format(company, branch_name, branch_amount))
            branch_ = {'company': company, 'branch_name': branch_name, 'branch_amount': branch_amount}
            branch_list.append(branch_)
        collection.insert_many(branch_list)
    except Exception as e:
        print(e)
    finally:
        time.sleep(5)


def manage():
    for i in company_list(file):
        print(get_unique_key(url=i))
        branch(url=get_unique_key(url=i))


if __name__ == '__main__':
    manage()