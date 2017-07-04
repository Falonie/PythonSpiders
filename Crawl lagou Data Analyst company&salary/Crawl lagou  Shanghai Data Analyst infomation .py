import requests, re, time, csv, pymysql, pymongo
from bs4 import BeautifulSoup
from lxml import html

cookie = {
    'Cookie': 'user_trace_token=20170326001734-ec41389ced6b4a4882609bf9e467bdb2; LGUID=20170326001734-8e3315f4-1176-11e7-9569-5254005c3644; TG-TRACK-CODE=deliver_guess; JSESSIONID=197AA9B8333FB8CB7DF60C237916266D; _putrc=43700CED3E324D1B; login=true; unick=%E7%8E%8B%E6%99%B4%E6%99%A8; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=5; _gat=1; LGSID=20170329210923-ee02d0e2-1480-11e7-a717-525400f775ce; LGRID=20170329214841-6b11e72a-1486-11e7-9574-5254005c3644; SEARCH_ID=81650aaa6c154f45a2b11a1d4107a646; index_location_city=%E4%B8%8A%E6%B5%B7; _ga=GA1.2.1946463376.1490458642; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1490458642; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1490795326'}
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}


def lagou(someurl):
    connection = pymysql.connect(host='localhost', user='root', password='1234', db='employee', charset='utf8mb4')
    with connection.cursor() as cursor:
        create_table = 'create table lagou_shanghai(COMPANY varchar(255),BLOCK varchar(45),EXPERIENCE varchar(45),' \
                       'INDUSTRY varchar(45),SALARY varchar(45),SLOWER_SALARY varchar(45),HIGHER_SALARY varchar(45))'
        cursor.execute(create_table)
        connection.commit()

    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client['employee']
    lagou = db['lagou']

    session = requests.session()
    position = []
    for i in range(1, 32):
        # session = requests.session()
        url = someurl.format(i)
        #    r = requests.get(url, cookies=cookie, headers=header).text
        r = session.get(url, cookies=cookie, headers=header).content
        bsobj = BeautifulSoup(r, 'html.parser')
        sel = html.fromstring(r)
        # pattern = re.compile(r'<span class="money">(.*?)</span>')
        # pattern2 = re.compile(r'class="con_list_item default_list" data-company=(.*?) data-companyid=')
        # pattern3 = re.compile(r'<span class="add">\[<em>(.*?)</em>\]')
        company_name = sel.xpath('//div[@class="company_name"]/a/text()')
        salary = sel.xpath('//span[@class="money"]/text()')
        block = sel.xpath('//div[@class="p_top"]/a/span/em/text()')
        experience = re.findall(r'<!--<i></i>-->(.*?)/', str(bsobj))
        industry = sel.xpath('//div[@class="industry"]/text()')
        print('Page %s' % i)
        for c, s, b, e, i in zip(company_name, salary, block, experience, industry):
            s1 = re.split(r'[-,以上]', s)[0]
            s2 = re.split(r'[-,以上]', s)[1]
            s1 = re.sub(r'[k,K]', '000', s1)
            s2 = re.sub(r'[k,K]', '000', s2)
            i = i.strip().split('/')[0]
            print(c, e, b, i, s, s1, s2)
            with open('lagou.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow((c, e, b, i, s, s1, s2))

            with connection.cursor() as cursor:
                sql = 'insert into lagou_shanghai (COMPANY,SALARY,SLOWER_SALARY,HIGHER_SALARY,EXPERIENCE,BLOCK,INDUSTRY) values(%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql, (c, s, s1, s2, e, b, i))
                connection.commit()

            job = {'company': c, 'experience': e, 'block': b, 'industry': i, 'salary': s, 'lower salary': s1,
                   'higher salary': s2}
            position.append(job)
    db['lagou'].insert_many(position)

if __name__ == '__main__':
    base_url = 'https://www.lagou.com/zhaopin/shujufenxishi/{}/?filterOption=3'
    lagou(base_url)