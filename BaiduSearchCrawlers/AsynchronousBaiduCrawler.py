import re, xlrd, time, csv, asyncio, aiohttp, pymongo
from lxml import html

file = '/media/salesmind/Other/baidu_homepage_search/官网_test2.xlsx'
file2 = r'E:\baidu_homepage_search\官网_test.xlsx'
base_url = 'http://www.baidu.com/s?q1={}@V'
collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['Baidu_Search']


async def asynchronous_baidu_search(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # print(await response.text())
            company_name = re.findall('q1=(.*?)@V', url)[0]
            search_result = []
            selector = html.fromstring(await response.text())
            try:
                search_item = selector.xpath('//div[@class="ecl-vmp-card2"]/div[@class="ecl-vmp-contianer c-border"]/'
                                             'div[@class="c-row section header-section"]/h2/text()')
                # search_item2 = re.findall(r'<h2 class="c-gap-bottom">(.*?)</h2>', response)
                link = selector.xpath('//div[@class="c-row section main-section last"]/'
                                      'div[1]/table/tr[2]/td/a[1]/text()')[0]
                link = re.sub('\xa0', '', link)
                # search_result.append([company_name, search_item[0], link])
                result = {'company_name': company_name, 'search_item': search_item[0], 'link': link,
                          'authentication': True}
                search_result.append(result)
            except:
                for i in selector.xpath('//div[@id="content_left"]/div[position()<7]'):
                    search_item = ''.join(str(i).strip() for i in i.xpath('h3/a/descendant::text()'))
                    link = i.xpath('div/div[@class="c-span18 c-span-last"]/div[@class="f13"]/a/descendant::text()|'
                                   'div[@class="f13"]/a/text()|div/div[2]/p[2]/span[1]/text()')
                    link = [''.join(str(i).strip() for i in link).replace('百度快照', '')]
                    if not link:
                        link = ['']
                    link = re.sub('\xa0', '', link[0])
                    # result = [company_name, search_item, link]
                    result = {'company_name': company_name, 'search_item': search_item, 'link': link,
                              'authentication': False}
                    search_result.append(result)
            finally:
                print(search_result)
                # results_ = [{'search_item': j[0], 'search_result': j[1], 'link': j[2]} for j in search_result]
                try:
                    collection.insert_many(search_result)
                except Exception as e:
                    print(e)
                    # with open('baidu_search_result.csv', 'a+') as f:
                    #     writer = csv.writer(f)
                    #     writer.writerows(search_result)


def company_list(file):
    with xlrd.open_workbook(file) as data:
        table = data.sheets()[0]
        company_list_ = [table.row_values(rownum)[0] for rownum in range(1, table.nrows)]
        return company_list_


if __name__ == '__main__':
    t0 = time.time()
    company_urls = [base_url.format(i) for i in company_list(file=file)]
    tasks = [asynchronous_baidu_search(url) for url in company_urls]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    print(time.time() - t0)
    pass