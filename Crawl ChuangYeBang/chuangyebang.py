import requests, re, csv, pymysql, time, os
from bs4 import BeautifulSoup
from lxml import html
from itertools import zip_longest

baseurl = 'http://www.cyzone.cn/event/list-764-0-{}-0-0-0-0/'
url = 'http://www.cyzone.cn/event/list-764-0-3-0-0-0-0/'
cookie = {
    'Cookie': 'BAIDU_SSP_lcr=https://www.google.com.hk/; __utma=22723113.1992140974.1496203791.1496213503.1496220940.3; __utmc=22723113; __utmz=22723113.1496220940.3.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmv=22723113.|1=user=null_null=1; Hm_lvt_5f6b02d88ea6aa37bfd72ee1b554bf6f=1496203790,1496213503,1496220940; Hm_lpvt_5f6b02d88ea6aa37bfd72ee1b554bf6f=1496221033'}
header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Encoding': 'gzip, deflate, sdch', 'Accept-Language': 'zh-CN,zh;q=0.8',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}


def chuangyebang():
    downloadpath = 'E:\chuangyebang_logo'
    if not os.path.exists(downloadpath):
        os.mkdir(downloadpath)
    else:
        pass

    connection = pymysql.connect(host='localhost', user='root', password='1234', db='employee', charset='utf8mb4')
    session = requests.session()

    for i in range(1, 890):
        url = baseurl.format(i)
        response = session.get(url=url, headers=header, cookies=cookie).text
        sel = html.fromstring(response)
        items = sel.xpath('//tr[@class="table-plate3"]')
        print('page {}'.format(i))
        for item in items:
            investors = item.xpath('td[@class="tp3"]/@title')[0]
            investor = re.sub(r'[\t\r\n,]', '', investors).replace(' ', '')
            product_name = item.xpath('td[@class="tp2"]/span[@class="tp2_tit"]/a/text()')[0]
            company = ''.join([str(i) for i in item.xpath('td[@class="tp2"]/span[@class="tp2_com"]/text()')])
            financial_amount = ''.join(str(i) for i in item.xpath('td[3]/div[@class="money"]/text()'))
            rounds = ''.join(str(i) for i in item.xpath('td[4]/text()'))
            industry = ''.join(str(i) for i in item.xpath('td[last()-2]/a/text()'))
            times = ''.join(str(i) for i in item.xpath('td[last()-1]/text()'))
            image_path = item.xpath('td[1]/a/img/@src')[0]
            image = session.get(image_path).content
            print(product_name, company, financial_amount, rounds, investor, industry, times, image_path)
            filename = '{}_{}_.jpg'.format(product_name, company)
            file = downloadpath + '\\' + filename

            try:
                with open(file, 'wb') as f:
                    f.write(image)
            except Exception as e:
                print(e)

            try:
                with open('chuangyebang.csv', 'a+', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow((product_name, company, financial_amount, rounds, investor, industry, times))
            except Exception as e:
                pass

            with connection.cursor() as cursor:
                sql = 'insert into chuangyebang (PRODUCT_NAME,COMPANY_NAME,AMOUNT,ROUNDS,INVESTORS,INDUSTRY,TIME) values (%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql, (product_name, company, financial_amount, rounds, investor, industry, times))
                connection.commit()
        time.sleep(5)
    time.sleep(5.5)


if __name__ == '__main__':
    chuangyebang()