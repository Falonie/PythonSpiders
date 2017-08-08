import requests, re, pymysql
from bs4 import BeautifulSoup
from lxml import html, etree

base_url = 'https://www.amazon.com/s/ref=sr_pg_{page}?rh=n%3A283155%2Ck%3Apython&page={page}&keywords=python&ie=UTF8&qid=1493708663&spIA=1785883801,B01MS5MBPQ,1784398632,B01ATC5SQY,1786464470,B01MZ5X8QQ,B071RKKQTW,178646439X,B01MS6NN02,B01M63XMN1'
url_cn = 'https://www.amazon.cn/s/ref=nb_sb_ss_c_2_6?__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=search-alias%3Dbooks&field-keywords=python&sprefix=python%2Caps%2C149&crid=QYYUOSU48MQU'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
cookie = {
    'Cookie': 'session-token=f8xAgLueBhn9NCL0gpB048RXVzNkWuDnR+Qya6Wu7Zkz6Y831ogI4ftVSnvSVkAWH5ngYgVppgpvPg3Fjin203H4h6UpLBvwYbwuzf6SZGnYAXO51P2TtArNy/zMZr0FdSwm7nQIDnSjhsbpC2V8MVXlSHcbQ4/023HJZDIbsREo7KEd942p6j4l3Igv/oTJ; x-wl-uid=1GYh/oY10ZWNjqqmYG7mrEkboksY1LoZD0y/RpHmhZ8M/jFyqksWg0JOSBro6U+xTnVg4cxiLkzg=; skin=noskin; JSESSIONID=27E42C46E14D9A6166A39323CB256E92; session-id-time=2082787201l; session-id=159-4015366-6650112; ubid-main=160-7552422-4139833; csm-hit=ZFMXG7B4A0MYJWN39E1J+sa-ZFMXG7B4A0MYJWN39E1J-KG72V5XKQ5RZ241J79XQ|1492441072302'}


def amazon():
    connnection = pymysql.connect(host='localhost', user='root', password='1234', db='employee', charset='utf8mb4')
    with connnection.cursor() as cursor:
        cursor.execute('create table amazon (BOOKNAME VARCHAR(256),RATING INT,PRICE VARCHAR(45))')
        connnection.commit()

    for i in range(1, 10):
        session = requests.session()
        url = base_url.format(page=i)
        response = session.get(url, headers=header, cookies=cookie).text
        bsobj = BeautifulSoup(response, 'html.parser')
        sel = etree.HTML(response)
        # sel=html.fromstring(response)
        books = sel.xpath('//h2[@data-attribute]/text()')
        rating = sel.xpath('//div[@class="a-row a-spacing-mini"]/a/text()')
        whole_price = sel.xpath('//span[@class="sx-price sx-price-large"]/span[@class="sx-price-whole"]/text()')
        fractional_price = sel.xpath(
            '//span[@class="sx-price sx-price-large"]/sup[@class="sx-price-fractional"]/text()')
        price = sel.xpath('//div[@class="a-column a-span7"]/div[@class="a-row a-spacing-none"][2]/a/span/@aria-label')
        publish_date = sel.xpath(
            '//div[@class="a-row a-spacing-small"]/div[@class="a-row a-spacing-none"][1]/span[@class="a-size-small a-color-secondary"]/text()')
        # authors=sel.xpath('//div[@class="a-row a-spacing-small"]/div[@class="a-row a-spacing-none"][2]/text()')
        # author=sel.xpath('//div[@class="a-row a-spacing-small"]/div[@class="a-row a-spacing-none"][2]/span/text()')
        print('page %s' % i)
        for b, r, p in zip(books, rating, price):
            print(b, r, p)

            with connnection.cursor() as cursor:
                sql = 'insert into amazon (BOOKNAME,RATING,PRICE) values (%s,%s,%s)'
                cursor.execute(sql, (b, r, p))
                connnection.commit()


if __name__ == '__main__':
    amazon()