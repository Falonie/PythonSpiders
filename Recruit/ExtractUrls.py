import asyncio, aiohttp, pymongo, time, itertools
from lxml import html

collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['recruit_urls_shenzhen_sales_representative']


async def extract_urls(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=None) as response:
            sel = html.fromstring(await response.text())
            # urls = [_ for _ in sel.xpath('//div[@id="resultList"]/div[@class="el"]/p/span/a/@href')]
            urls = [{'url': _} for _ in sel.xpath('//div[@id="resultList"]/div[@class="el"]/p/span/a/@href')]
            try:
                collection.insert_many(urls)
            except Exception as e:
                print(e)
            print(urls)
            return urls


def main():
    t0 = time.time()
    url = 'http://search.51job.com/list/040000,000000,0000,00,9,99,%25E9%2594%2580%25E5%2594%25AE,2,{}.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=1&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    urls = [url.format(_) for _ in range(1, 2001)]
    tasks = [extract_urls(url) for url in urls]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*tasks))
    # try:
    #     collection.insert_many(results)
    # except Exception as e:
    #     print(e)
    # print(results, len(results))
    loop.close()
    print(time.time() - t0)


if __name__ == '__main__':
    main()
