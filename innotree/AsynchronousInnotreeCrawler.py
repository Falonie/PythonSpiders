import re, xlrd, time, csv, asyncio, aiohttp, pymongo
from lxml import html

db = pymongo.MongoClient(host='localhost', port=27017)['Falonie']
collection = db['innotree_成长期_filter_duplicates_crawled_result_asyncio']
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
cookies = {
    'Cookie': '_user_identify_=e313a20b-54d9-3f38-b557-6887837deb3b; JSESSIONID=aaa1ZkdbIeOHLa9YlHTbw; uID=461384; sID=85ca7d607d707ee79eeb62c0865e5acb; Hm_lvt_ddf0d99bc06024e29662071b7fc5044f=1513665906; Hm_lpvt_ddf0d99bc06024e29662071b7fc5044f=1513666063; Hm_lvt_37854ae85b75cf05012d4d71db2a355a=1513665907; Hm_lpvt_37854ae85b75cf05012d4d71db2a355a=1513666063'}
file = 'innotree_成熟期_filter_duplicates.xlsx'


async def asynchronous_baidu_search(url):
    async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
        async with session.get(url) as response:
            selector = html.fromstring(await response.text())
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
            brief_intro = re.sub('[\n\xa0 ]', '', ''.join(str(i).strip() for i in brief_intro))
            investment = selector.xpath('//div[@class="de_170822_d01_d03"]/table/tr/td/descendant::text()')
            investment = ''.join(str(i).strip() for i in investment)
            leadership = selector.xpath(
                '//div[@class="de_170822_d01_d05 de_170822_d01_d05_ov"]/table/tr/td[position()>1]/span/text()')
            leadership = ''.join(str(i).strip() for i in leadership)
            item_dict.update(
                {'brief_intro': brief_intro, 'investment': investment, 'leadership': leadership, 'tags': tags,
                 'product': product, 'logo_url': logo_url, 'url': url})
            collection.insert(item_dict)
            return item_dict


def read_excel(file):
    with xlrd.open_workbook(file) as data_:
        table = data_.sheets()[0]
        # for rownum in range(0, table.nrows):
        #     row = table.row_values(rownum)
        #     yield row[0]
        urls_list = [table.row_values(rownum)[0] for rownum in range(0, table.nrows)]
        return urls_list


def main():
    t0 = time.time()
    # company_urls = [base_url.format(i) for i in company_list(file=file)]
    tasks = [asynchronous_baidu_search(url) for url in read_excel(file)]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    print(time.time() - t0)


if __name__ == '__main__':
    t0 = time.time()
    # company_urls = [base_url.format(i) for i in company_list(file=file)]
    tasks = [asynchronous_baidu_search(url) for url in read_excel(file)]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    print(time.time() - t0)
    # main()
    # print(read_excel(file))