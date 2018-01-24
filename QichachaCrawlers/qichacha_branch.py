import requests, re, pymongo, time, xlrd, logging
from lxml import html

url = 'http://www.qichacha.com/company_getinfos?unique=518ef3a4b4a0ae4e6a58f8d288bdfd28&companyname=%E5%8C%97%E4%BA%AC%E7%A5%9E%E5%B7%9E%E6%95%B0%E7%A0%81%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&tab=base'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
cookies = {
    'Cookie': 'acw_tc=AQAAABgFeicdRw0Ao/ycy0O1A1zlaoSI; PHPSESSID=ccga6okdop91ge6b34054hb766; UM_distinctid=160fcf6271d506-0ba8b283e8d2a2-3a760e5d-100200-160fcf6271e416; zg_did=%7B%22did%22%3A%20%22160fcf6273736c-0f5f15548cac9f-3a760e5d-100200-160fcf627387e3%22%7D; _uab_collina=151607248499256448881892; CNZZDATA1254842228=970305631-1516067880-%7C1516758123; _umdata=0712F33290AB8A6D7200D5AC434E5E0348CEA517391D874DCBE66267A34DEBCA17C85FDAA43E1B63CD43AD3E795C914C10C8ABF08DECF94385023B407D7D3633; hasShow=1; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516759542045%2C%22updated%22%3A%201516761517720%2C%22info%22%3A%201516696506138%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%228df61d213235daf577fa1bf530ea2748%22%7D'}
# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S: %p', level=logging.DEBUG)
collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['壳牌-基础-487-01.24_branch_test']
file = r'/media/salesmind/000CFFD8000DB949/Ctrip/壳牌-基础-487-01.24_insurance.xlsx'
session = requests.session()


def company_list_txt(file):
    with open(file, 'r') as f:
        for i, line in enumerate(f.readlines(), 1):
            # print(i,line.strip())
            yield 'http://www.qichacha.com/search?key={}'.format(line.strip())


def company_list_excel(file):
    with xlrd.open_workbook(file) as data:
        table = data.sheets()[0]
        for rownum in range(0, table.nrows):
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


def branch_old(url):
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
            # print(company,branch_name,branch_amount)
            logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S: %p', level=logging.DEBUG)
            logging.info(msg='{0},{1},{2}'.format(company, branch_name, branch_amount))
            branch_ = {'company': company, 'branch_name': branch_name, 'branch_amount': branch_amount}
            branch_list.append(branch_)
        # collection.insert_many(branch_list)
    except Exception as e:
        print(e)
    finally:
        time.sleep(5)


def branch(url):
    response = requests.get(url=url, headers=headers, cookies=cookies).text
    sel = html.fromstring(response)
    pattern = re.compile(r'companyname=(.*?)&')
    company = pattern.findall(url)[0]
    branch_amount = sel.xpath('//*[@id="Subcom"]/div[1]/span[2]/text()')
    branch_amount = ''.join(str(i).strip() for i in branch_amount)
    items = []
    for _ in sel.xpath('//section[@id="Subcom"]/table[@class="ntable"]/tr'):
        branch1 = _.xpath('td[position()=1 or position()=2]/descendant::text()')
        branch1 = ''.join(str(i).strip() for i in branch1)
        branch2 = _.xpath('td[position()=3 or position()=4]/descendant::text()')
        branch2 = ''.join(str(i).strip() for i in branch2)
        item = [{'company': company, 'branch_name': branch1, 'branch_amount': branch_amount},
                {'company': company, 'branch_name': branch2, 'branch_amount': branch_amount}]
        items.extend(item)
    collection.insert_many(items)
    return items


def manage():
    for i in company_list_excel(file):
        print(get_unique_key(url=i))
        try:
            print(branch(url=get_unique_key(url=i)))
        except Exception as e:
            print(e)


if __name__ == '__main__':
    manage()