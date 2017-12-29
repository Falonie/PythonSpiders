import requests, re, time, pymongo, pymysql, csv, logging, random, xlrd
from lxml import html

header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
cookie = {
    'Cookie': '_uab_collina=150527284704149589548835; UM_distinctid=15ea3addeae8d3-07742f025e0c8f-3976045e-13c680-15ea3addeafa93; acw_tc=AQAAAFfUzllKIg8Ao/ycy6gTQF9ma42b; hasShow=1; _umdata=E2AE90FA4E0E42DE0F446AE0957BCA8A133E0B34391C28947685CA351FCA05F1C03BAF7D07039AA4CD43AD3E795C914C691365682D841235663C5E6D1DA20EAD; PHPSESSID=4o1bpmdaq17fpftpqn6lnieh14; zg_did=%7B%22did%22%3A%20%2215e7940da0f78f-01ffe099dc343d-3976045e-13c680-15e7940da10ba7%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201513855130216%2C%22updated%22%3A%201513855268686%2C%22info%22%3A%201513855130220%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22dad2b2131a760fad57cbbb67ceea827c%22%7D; CNZZDATA1254842228=1726320973-1505979679-%7C1513850084'}
lawsuit_collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie']['lawsuit_test']
session = requests.session()
file = r'/media/salesmind/Other/cloud_bird/test_company.xlsx'


class Lawsuit(object):
    def company_list_txt(self, file):
        with open(file, 'r') as f:
            for i, line in enumerate(f.readlines(), 1):
                # print(i,line.strip())
                self.line = line.strip()
                yield 'http://www.qichacha.com/search?key={}'.format(self.line)

    def company_list_excel(self, file):
        with xlrd.open_workbook(file) as data:
            table = data.sheets()[0]
            for rownum in range(1, table.nrows):
                row = table.row_values(rownum)
                yield 'http://www.qichacha.com/search?key={}'.format(str(row[0]).strip())

    def get_unique_key(self, url):
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

    def lawsuit(self, url):
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
                    requests.get(url=base_url.format(page=page_num).split('&box')[0], headers=header,
                                 cookies=cookie).text)
                lose_credit = sel.xpath('//*[@id="shixinlist"]/div[1]/descendant::text()')
                lose_credit = ''.join(str(i).strip() for i in lose_credit)
                for i in selector.xpath('//table[@class="m_changeList"]/tr[position()>1]'):
                    lawsuit = i.xpath('td[2]/descendant::text()')
                    lawsuit_name = ''.join(str(i).strip() for i in lawsuit)
                    id_ = ''.join(str(_) for _ in i.xpath('td[2]/a/@onclick'))
                    lawsuit_documnet_id = re.search(r'"(.*?)"', id_).group(1)
                    data = {'id': lawsuit_documnet_id}
                    documnet_url = 'http://www.qichacha.com/company_wenshuView'
                    selector = html.fromstring(
                        session.post(url=documnet_url, data=data, headers=header, cookies=cookie).json()['data'])
                    lawsuit_documnet = selector.xpath('//div/descendant::text()')
                    lawsuit_documnet = re.sub(r'[\u3000\xa0]', '', ''.join(str(i).strip() for i in lawsuit_documnet))
                    # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S: %p',
                    #                     level=logging.DEBUG)
                    # logging.info(msg='{0},{1},{2},{3}'.format(company, lawsuit_name,wenshu_id, lose_credit))
                    # with connection.cursor() as cursor:
                    #     sql = "INSERT INTO qichacha_recruit (company,recruit) VALUES ('{}','{}')"
                    #     # sql = 'insert into qichacha_recruit (recruit) VALUES (%s)'
                    #     cursor.execute(query=sql.format(company, b))
                    #     # cursor.execute(sql,(b))
                    #     connection.commit()
                    lawsuit_item = {'company': company, 'company_input': self.line, 'lawsuit_name': lawsuit_name,
                                    'lawsuit_documnet': lawsuit_documnet, 'lose credit': lose_credit}
                    print(lawsuit_item)
                    position.append(lawsuit_item)
                lawsuit_collection.insert_many(position)
                page_num += 1
                time.sleep(12)
            except Exception as e:
                break
            finally:
                time.sleep(5)


def manage():
    lawsuit = Lawsuit()
    # print(list(company_list()))
    for i in lawsuit.company_list_excel(file=file):
        # print(i)
        print(lawsuit.get_unique_key(url=i))
        lawsuit.lawsuit(url=lawsuit.get_unique_key(url=i))


if __name__ == '__main__':
    manage()
    pass