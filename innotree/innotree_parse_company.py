import requests, time, pymongo, xlrd, re
from lxml import html
# from selenium import webdriver
from multiprocessing import Pool
from pprint import pprint

file = 'innotree_早期_filter_duplicates.xlsx'
db = pymongo.MongoClient(host='localhost', port=27017)['Falonie']
collection_read = db['innotree_beijing_zhongzi_filter_duplicates']
collection = db['innotree_战略并购_filter_duplicates_crawled_result']
# pprint(test_list)
# pprint([url.setdefault('product_url') for url in test_list])
urls = ['https://www.innotree.cn/inno/company/4957871552628651946.html',
        'https://www.innotree.cn/inno/company/6354892653699219687.html',
        'https://www.innotree.cn/inno/company/10548078748520937734.html',
        'https://www.innotree.cn/inno/company/1183084103595171085.html',
        'https://www.innotree.cn/inno/company/999980423478866118.html',
        'https://www.innotree.cn/inno/company/10005682308130865808.html',
        'https://www.innotree.cn/inno/company/7609729055695446200.html',
        'https://www.innotree.cn/inno/company/12044156300577152751.html',
        'https://www.innotree.cn/inno/company/4020570908260780691.html',
        'https://www.innotree.cn/inno/company/10151547046756713819.html']
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
cookies = {
    'Cookie': '_user_identify_=c0f7da20-b04b-32f5-bbe9-a7108b142fe2; JSESSIONID=aaa4JO2dYh7_IhltXkVbw; uID=461384; sID=ac8644df9ef12aced13b7d87b0570e42; Hm_lvt_37854ae85b75cf05012d4d71db2a355a=1513664777; Hm_lpvt_37854ae85b75cf05012d4d71db2a355a=1513758660; Hm_lvt_ddf0d99bc06024e29662071b7fc5044f=1513664777; Hm_lpvt_ddf0d99bc06024e29662071b7fc5044f=1513758660'}


def read_excel(file):
    with xlrd.open_workbook(file) as data_:
        table = data_.sheets()[0]
        # for rownum in range(0, table.nrows):
        #     row = table.row_values(rownum)
        #     yield row[0]
        urls_list = [table.row_values(rownum)[0] for rownum in range(0, table.nrows)]
        return urls_list


def read_excel_(file):
    with xlrd.open_workbook(file) as data_:
        table = data_.sheets()[0]
        # for rownum in range(0, table.nrows):
        #     row = table.row_values(rownum)
        #     yield row[0]
        urls_list = [table.row_values(rownum)[0] for rownum in range(6001, table.nrows)]
        return urls_list


def read_mongodb():
    collection = db['innotree_战略并购_filter_duplicates']
    # for j in collection.find({}):
    #     yield j
    return [_['url'] for _ in collection.find({})]


def parse_company(url):
    selector = html.fromstring(requests.get(url=url, headers=headers,).text)
    item_dict = {}
    for _ in selector.xpath('//div[@class="de_170822_d01_d"]/table'):
        title = _.xpath('tr/td[position()=1 or position()=3]/span/text()')
        text = _.xpath('tr/td[position()=2 or position()=4]/span/text()')
        item_dict.update({k: v for k, v in zip(title, text)})
    for _ in selector.xpath('//div[@class="mech_170525_nav"]/table/tr/td[2]/div'):
        province = _.xpath('a[1]/text()')
        province = ''.join(str(i).strip() for i in province)
        homepage = _.xpath('a[2]/text()')
        homepage = ''.join(str(i).strip() for i in homepage)
        item_dict.update({'province': province, 'homepage': homepage})
    logo_url = selector.xpath('//div[@class="mech_170525_nav"]/table/tr/td[1]/img/@src')
    logo_url = ''.join(str(i).strip() for i in logo_url)
    product = selector.xpath('//h3[@class="mech_170525_nav_h3"]/descendant::text()')
    product = ''.join(str(i).strip() for i in product)
    tags = selector.xpath('//div[@class="mech_170525_nav_d01"]/span/a/text()')
    brief_intro = selector.xpath('//div[@class="de_170822_d01_d02"]/descendant::text()')
    brief_intro = re.sub('[\n\xa0\r ]', '', ''.join(str(i).strip() for i in brief_intro))
    investment = selector.xpath('//div[@class="de_170822_d01_d03"]/table/tr/td/descendant::text()')
    investment = ''.join(str(i).strip() for i in investment)
    leadership = selector.xpath(
        '//div[@class="de_170822_d01_d05 de_170822_d01_d05_ov"]/table/tr/td[position()>1]/span/text()')
    leadership = ''.join(str(i).strip() for i in leadership)
    item_dict.update({'brief_intro': brief_intro, 'investment': investment, 'leadership': leadership, 'tags': tags,
                      'product': product, 'logo_url': logo_url, 'url': url})
    # collection.insert(item_dict)
    return item_dict


def main():
    t0 = time.time()
    with Pool() as pool:
        # p = pool.map(parse_company, read_excel(file))
        p = pool.map(parse_company, read_mongodb())
        for i, j in enumerate(p, 1):
            print(i, j)
            # try:
            #     collection.insert(j)
            # except Exception as e:
            #     print(e)
        try:
            collection.insert_many(p)
        except Exception as e:
            print(e)
    print(time.time() - t0)


def main_excel():
    # innotree = Innotree()
    for i, j in enumerate(read_excel(file), 1):
        print(i, parse_company(j))
        time.sleep(10)


if __name__ == '__main__':
    # print(parse_company('https://www.innotree.cn/inno/company/6354892653699219687.html'))
    main()
    # innotree = Innotree()
    # main_excel()
    # print(read_mongodb().__len__())
    # for i, j in enumerate(read_mongodb(), 1):
    #     print(i, j['url'])
    #     print(parse_company(j['url']))
    # for i, j in enumerate(read_excel(file), 1):
    #     print(i, j)
    # print(read_excel(file).__len__())