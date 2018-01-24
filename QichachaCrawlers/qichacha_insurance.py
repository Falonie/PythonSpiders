import requests, re, pymongo, time, xlrd, logging, os
from lxml import html, etree

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}
cookies = {
    'Cookie': 'acw_tc=AQAAABgFeicdRw0Ao/ycy0O1A1zlaoSI; PHPSESSID=ccga6okdop91ge6b34054hb766; UM_distinctid=160fcf6271d506-0ba8b283e8d2a2-3a760e5d-100200-160fcf6271e416; zg_did=%7B%22did%22%3A%20%22160fcf6273736c-0f5f15548cac9f-3a760e5d-100200-160fcf627387e3%22%7D; _uab_collina=151607248499256448881892; CNZZDATA1254842228=970305631-1516067880-%7C1516758123; _umdata=0712F33290AB8A6D7200D5AC434E5E0348CEA517391D874DCBE66267A34DEBCA17C85FDAA43E1B63CD43AD3E795C914C10C8ABF08DECF94385023B407D7D3633; hasShow=1; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201516759542045%2C%22updated%22%3A%201516759985479%2C%22info%22%3A%201516696506138%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%228df61d213235daf577fa1bf530ea2748%22%7D'}
# logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S: %p', level=logging.DEBUG)
collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['壳牌-基础-487-01.24_insurance_test']
url = 'http://www.qichacha.com/company_getinfos?unique=b125bab46af5f12bb648f1df588fce96&companyname=%E5%8C%97%E4%BA%AC%E4%B8%83%E8%A7%86%E9%87%8E%E6%96%87%E5%8C%96%E5%88%9B%E6%84%8F%E5%8F%91%E5%B1%95%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&tab=report'
file = r'/media/salesmind/000CFFD8000DB949/Ctrip/壳牌-基础-487-01.24_insurance.xlsx'


class Qichacha_insurance(object):
    def company_list_txt(self, file):
        with open(file, 'r') as f:
            for i, line in enumerate(f.readlines(), 1):
                # print(i,line.strip())
                self.row = line.strip()
                yield 'http://www.qichacha.com/search?key={}'.format(self.row)

    def company_list_excel(self, file):
        with xlrd.open_workbook(file) as data:
            table = data.sheets()[0]
            for rownum in range(0, table.nrows):  # 修改公司序号
                self.row = table.row_values(rownum)
                yield 'http://www.qichacha.com/search?key={}'.format(str(self.row[0]).strip())

    def get_unique_key(self, url):
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

    def parse_insurance(self, url):
        report_all = []
        insurance = {}
        try:
            sessoin = requests.session()
            r = sessoin.get(url=url, headers=headers, cookies=cookies).text
            # print(r)
            selector = html.fromstring(r)
            pattern = re.compile(r'companyname=(.*?)&')
            company = pattern.findall(url)[0]
            insurance.update({'company': company})
            for _ in selector.xpath('//div[@class="tab-pane fade in active"]/table[last()]/tbody/tr[position()<4]'):
                title = _.xpath('td[position()=1 or position()=3]/text()')
                content = _.xpath('td[position()=2 or position()=4]/text()')
                insurance.update({str(i).strip(): j for i, j in zip(title, content)})
                # annual_report.update({'company': company})
            insurance.update({'company_input': self.row[0],'status':'crawled'})
            report_all.append(insurance)
            collection.insert_many(report_all)
        except Exception as e:
            print(e)
        finally:
            return report_all


def manage():
    insurance = Qichacha_insurance()
    for i in insurance.company_list_excel(file):
        print(insurance.get_unique_key(i))
        print(insurance.parse_insurance(url=insurance.get_unique_key(url=i)))
        time.sleep(10)


if __name__ == '__main__':
    manage()