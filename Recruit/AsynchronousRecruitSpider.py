# -*- coding: utf-8 -*-
__author__ = 'Falonie'
import re
import asyncio
import aiohttp
import pymongo
import time
import xlrd
from lxml import html

collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['recruit_shenzhen_sales_representative']


async def crawl_recruit(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=None) as response:
            sel = html.fromstring(await response.text())
            item = {}
            for _ in sel.xpath('//div[@class="tHeader tHjob"]/div[@class="in"]/div[@class="cn"]'):
                position = _.xpath('h1/@title')
                item['position'] = ''.join(str(i) for i in position)
                location = _.xpath('span/text()')
                item['location'] = ''.join(str(i) for i in location)
                company = _.xpath('p[@class="cname"]/a/@title')
                item['company'] = ''.join(str(i) for i in company)
                industry = _.xpath('p[@class="msg ltype"]/text()')
                nature_ = ''.join(str(i).strip() for i in industry)
                try:
                    item['nature'], item['scale'], item['industry'] = re.sub(r'[\r\t\xa0 ]', '', nature_).split('|')
                except Exception as e:
                    item['nature'], item['scale'], item['industry'] = re.sub(r'[\r\t\xa0 ]', '', nature_).split('|'), '', ''
            for _ in sel.xpath('//div[@class="jtag inbox"]/div[@class="t1"]'):
                # recruit_members = _.xpath('span[2]/descendant::text()')
                # recruit_members = ''.join(str(i) for i in recruit_members)
                # release_time = _.xpath('span[3]/descendant::text()')
                # release_time = ''.join(str(i) for i in release_time)
                recruit_members_release_time = _.xpath('span[position()<5]/text()')
                for i in recruit_members_release_time:
                    # recruit_members_=i if str(i).startswith('招') else ''
                    recruit_members = i if str(i).endswith('人') else ''
                    release_time = i if str(i).endswith('发布') else ''
                    item.update({'recruit_members': recruit_members, 'release_time': release_time})
                item['recruit_members_release_time'] = ','.join(str(i) for i in recruit_members_release_time)
                contact = sel.xpath('//div[@class="tCompany_main"]/div[3]/descendant::text()')
                item['contact'] = re.sub(r'[\r\t\xa0\0x80\u3000 ]', '', ''.join(str(i).strip() for i in contact))
                company_info = sel.xpath('////div[@class="tCompany_main"]/div[4]/descendant::text()')
                item['company_info'] = re.sub(r'[\r\t\xa0\u3000\0x80 ]', '',
                                              ''.join(str(i).strip() for i in company_info))
                job_description = sel.xpath('//div[@class="tCompany_main"]/div[2]/descendant::text()')
                item['job_description'] = re.sub(r'[\r\t\xa0\0x80\u3000 ]', '',
                                                 ''.join(str(i).strip() for i in job_description))
                item['url'] = url
            print(item)
            try:
                collection.insert(item)
            except Exception as e:
                print(e)
            return item


def read_mongodb():
    collection_filter_duplicates = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['recruit_urls2']
    urls = [_['url'] for _ in collection_filter_duplicates.find({})]
    return urls


def read_excel(file):
    with xlrd.open_workbook(file) as data_:
        table = data_.sheets()[0]
        company_list_ = [table.row_values(rownum)[0] for rownum in range(99262, table.nrows)]
        return company_list_


def main_mongodb():
    t0 = time.time()
    tasks = [crawl_recruit(url) for url in read_mongodb()]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*tasks))
    # try:
    #     collection.insert_many(results)
    # except Exception as e:
    #     print(e)
    # print(results,len(results))
    loop.close()
    print(time.time() - t0)


def main_excel(file):
    t0 = time.time()
    tasks = [crawl_recruit(url) for url in read_excel(file)]
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*tasks))
    # try:
    #     collection.insert_many(results)
    # except Exception as e:
    #     print(e)
    # print(results,len(results))
    loop.close()
    print(time.time() - t0)


if __name__ == '__main__':
    main_excel('recruit_urls_shenzhen_sales_representative.xlsx')