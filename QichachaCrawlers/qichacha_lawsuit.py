import requests, re, time, pymongo, pymysql, csv, logging, random, xlrd
from lxml import html

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
cookie = {
    'Cookie': 'acw_tc=AQAAAKTc8GK7EgAAo/ycyzFO2mbih7Gu; UM_distinctid=15fc3be7c53a5-0a92c0bf8f304a-112b1709-13c680-15fc3be7c5424a; _uab_collina=151081756327655449988871; _umdata=65F7F3A2F63DF020F26352CB2D723F6947983530C33A3C5B703E522C5AAB7C1CA01A32ABB7CA0ECBCD43AD3E795C914C2053C5B223499DBB947E148B2D5581AE; PHPSESSID=njrm2b2gquobfttkbkbvsu7eh1; zg_did=%7B%22did%22%3A%20%2215fc3be7c733af-0df765ef22e6ad-112b1709-13c680-15fc3be7c74463%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201511228923753%2C%22updated%22%3A%201511228928703%2C%22info%22%3A%201510817561724%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%228df61d213235daf577fa1bf530ea2748%22%7D; CNZZDATA1254842228=1519393824-1510815399-%7C1511224464'}
# connection = pymysql.connect(host='localhost', user='root', password='1234', db='employee', charset='utf8mb4')
lawsuit_collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie']['lawsuit_test']
session = requests.session()
file = '/media/salesmind/Other/cloud_bird/test_company.xlsx'


# def company_list():
#     with open('/media/salesmind/Other/cloud_bird/lawsuit_test_companies.txt', 'r') as f:
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
        # base_url = 'http://www.qichacha.com/company_getinfos?unique={}&companyname={}&p=3&tab=susong&box=wenshu'
        time.sleep(5)
        return base_url.format(unique=unique_key, company=company_name) + '&p={page}&tab=susong&box=wenshu'


def lawsuit(url):
    page_num = 1
    base_url = url
    while True:
        position = []
        try:
            print('page {}'.format(page_num), base_url.format(page=page_num))
            r = session.get(url=base_url.format(page=page_num), headers=header, cookies=cookie)
            selector = html.fromstring(r.text)
            # print(r.text)
            pattern = re.compile(r'companyname=(.*?)&')
            company = pattern.findall(base_url)[0]
            print(base_url.format(page=page_num).split('&box')[0])
            sel = html.fromstring(
                requests.get(url=base_url.format(page=page_num).split('&box')[0], headers=header, cookies=cookie).text)
            lose_credit = sel.xpath('//*[@id="shixinlist"]/div[1]/descendant::text()')
            lose_credit = ''.join(str(i).strip() for i in lose_credit)
            for i in selector.xpath('//table[@class="m_changeList"]/tr[position()>1]'):
                lawsuit = i.xpath('td[2]/descendant::text()')
                lawsuit_name = ''.join(str(i).strip() for i in lawsuit)
                # print(company, b)
                logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S: %p',
                                    level=logging.DEBUG)
                logging.info(msg='{0},{1},{2}'.format(company, lawsuit_name, lose_credit))
                # with connection.cursor() as cursor:
                #     sql = "INSERT INTO qichacha_recruit (company,recruit) VALUES ('{}','{}')"
                #     # sql = 'insert into qichacha_recruit (recruit) VALUES (%s)'
                #     cursor.execute(query=sql.format(company, b))
                #     # cursor.execute(sql,(b))
                #     connection.commit()
                recruit_joblist = {'company': company, 'lawsuit_name': lawsuit_name, 'lose credit': lose_credit}
                position.append(recruit_joblist)
            lawsuit_collection.insert_many(position)
            page_num += 1
            time.sleep(12)
        except Exception as e:
            break
        finally:
            time.sleep(5)


def manage():
    # print(list(company_list()))
    for i in company_list(file=file):
        # print(i)
        print(get_unique_key(url=i))
        lawsuit(url=get_unique_key(url=i))


if __name__ == '__main__':
    manage()
    pass