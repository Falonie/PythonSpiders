import requests, re, pymongo, time, xlrd, logging
from lxml import html, etree

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
cookies = {
    'Cookie': 'acw_tc=AQAAAKTc8GK7EgAAo/ycyzFO2mbih7Gu; UM_distinctid=15fc3be7c53a5-0a92c0bf8f304a-112b1709-13c680-15fc3be7c5424a; _uab_collina=151081756327655449988871; _umdata=65F7F3A2F63DF020F26352CB2D723F6947983530C33A3C5B703E522C5AAB7C1CA01A32ABB7CA0ECBCD43AD3E795C914C2053C5B223499DBB947E148B2D5581AE; PHPSESSID=njrm2b2gquobfttkbkbvsu7eh1; zg_did=%7B%22did%22%3A%20%2215fc3be7c733af-0df765ef22e6ad-112b1709-13c680-15fc3be7c74463%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201511228923753%2C%22updated%22%3A%201511228928703%2C%22info%22%3A%201510817561724%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%228df61d213235daf577fa1bf530ea2748%22%7D; CNZZDATA1254842228=1519393824-1510815399-%7C1511224464'}
# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S: %p', level=logging.DEBUG)
collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['annual_report']
url = 'http://www.qichacha.com/company_getinfos?unique=4b9deda0d70708b85c80f282f0190986&companyname=%E4%B9%90%E5%AE%9C%E5%98%89%E5%AE%B6%E5%B1%85%E9%9B%86%E5%9B%A2%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&tab=report'
file = '/media/salesmind/Other/cloud_bird/test_company.xlsx'


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
        base_url = 'http://www.qichacha.com/company_getinfos?unique={unique}&companyname={company}&tab=report'
        time.sleep(5)
        return base_url.format(unique=unique_key, company=company_name)


def parse_annual_report(url):
    sessoin = requests.session()
    r = sessoin.get(url=url, headers=headers, cookies=cookies).text
    # print(r)
    selector = html.fromstring(r)
    pattern = re.compile(r'companyname=(.*?)&')
    company = pattern.findall(url)[0]
    report_all = []
    for i in selector.xpath('//div[@class="tab-pane fade in active" or @class="tab-pane fade in "]'):
        annual_report = {}
        year = i.xpath('@id')
        for _ in i.xpath('table[last()]/tr'):
            title = _.xpath('td[position()=1 or position()=3]/text()')
            content = _.xpath('td[position()=2 or position()=4]/text()')
            annual_report.update({str(i).strip(): j for i, j in zip(title, content)})
            # for i, j in zip(title, content):
            #     annual_report.update({str(i).strip(): j})
        annual_report.update({'year': year, 'company': company})
        # print(annual_report)
        report_all.append(annual_report)
    print(report_all)


def manage():
    for i in company_list(file):
        print(get_unique_key(i))
        parse_annual_report(url=get_unique_key(url=i))


if __name__ == '__main__':
    manage()
    # parse_annual_report(url=url)
    pass