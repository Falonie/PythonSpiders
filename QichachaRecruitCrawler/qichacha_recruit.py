import requests, re, time, pymongo, pymysql, csv
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
cookies = {
    'Cookie': 'acw_tc=AQAAAMd2HngF+gQAoPycy55jpR9twWwK; UM_distinctid=15e584568af2ef-03b728d384c188-474f0820-13c680-15e584568b03ec; _uab_collina=150471949933594258786047; PHPSESSID=plr0e6jkkv52m2mfbdpdphva43; _umdata=535523100CBE37C3EEE4F58012F07AE2F5400B3B4FEC5C11EE550AC11AE600EAAAE22A7B00C42407CD43AD3E795C914CD9B992F791E88C778FD650C880892382; zg_did=%7B%22did%22%3A%20%2215e584568900-082955edf3a97a-474f0820-13c680-15e584568913c4%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201504747854927%2C%22updated%22%3A%201504753355577%2C%22info%22%3A%201504719497367%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%22eec241ef4431df98337f2759c6cd7538%22%7D; CNZZDATA1254842228=2113774111-1504743592-%7C1504781394'}
connection = pymysql.connect(host='localhost', user='root', password='1234', db='employee', charset='utf8mb4')
recruit_collection = pymongo.MongoClient(host='localhost', port=27017)['employee']['qichacha_recruit']
session = requests.session()


def company_list():
    with open('E:\OTMS\otms招聘职位采集.txt', 'r') as f:
        for i, line in enumerate(f.readlines(), 1):
            # print(i,line.strip())
            yield 'http://www.qichacha.com/search?key={}'.format(line.strip())


def get_unique_key(url):
    response = session.get(url=url, headers=headers, cookies=cookies).text
    selector = html.fromstring(response)
    company_name = selector.xpath('//*[@id="searchlist"]/table[1]/tbody/tr[1]/td[2]/a/em/em/text()|//*[@id="searchlist"]/table[1]/tbody/tr[1]/td[2]/a/em/text()')[0]
    href = selector.xpath('//*[@id="searchlist"]/table[1]/tbody/tr/td[2]/a/@href')[0]
    unique_key = re.split(r'[_.]', href)[1]
    # print(company_name, href, unique_key)
    base_url = 'http://www.qichacha.com/company_getinfos?unique={unique}&companyname={company}'  # &p={page}&tab=run&box=job'
    return base_url.format(unique=unique_key, company=company_name) + '&p={page}&tab=run&box=job'


# base_url = 'http://www.qichacha.com/company_getinfos?unique=24f03b2ac603ae4fb5fa995c212e3c37&companyname=%E5%A5%A5%E7%89%B9%E6%9C%97%E7%94%B5%E5%99%A8%EF%BC%88%E5%B9%BF%E5%B7%9E%EF%BC%89%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&p={page}&tab=run&box=job'
def recruit(url):
    page_num = 1
    base_url = url
    # base_url=get_unique_key()
    # base_url = url.format(page=page_num)
    # base_url = 'http://www.qichacha.com/company_getinfos?unique=24f03b2ac603ae4fb5fa995c212e3c37&companyname=%E5%A5%A5%E7%89%B9%E6%9C%97%E7%94%B5%E5%99%A8%EF%BC%88%E5%B9%BF%E5%B7%9E%EF%BC%89%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&p={page}&tab=run&box=job'
    while True:
        position = []
        try:
            print('page {}'.format(page_num), base_url.format(page=page_num))
            r = session.get(url=base_url.format(page=page_num), headers=headers, cookies=cookies)
            selector = html.fromstring(r.text)
            pattern = re.compile(r'companyname=(.*?)&')
            company = pattern.findall(base_url)[0]
            for i in selector.xpath('//table[@class="m_changeList"]/tbody/tr[position()>1]'):
                job = i.xpath('td/descendant::text()')
                b = ''.join(str(i).strip() for i in job)
                print(company, b)
                with connection.cursor() as cursor:
                    sql = "INSERT INTO qichacha_recruit (company,recruit) VALUES ('{}','{}')"
                    # sql = 'insert into qichacha_recruit (recruit) VALUES (%s)'
                    cursor.execute(query=sql.format(company, b))
                    # cursor.execute(sql,(b))
                    connection.commit()
                recruit_joblist = {'company': company, 'recruit_joblist': b}
                position.append(recruit_joblist)
            recruit_collection.insert_many(position)
            page_num += 1
            time.sleep(17)
        except Exception as e:
            break
        finally:
            time.time(7)

if __name__ == '__main__':
    # print(list(company_list()))
    for i in company_list():
        print(get_unique_key(url=i))
        recruit(url=get_unique_key(url=i))
    pass