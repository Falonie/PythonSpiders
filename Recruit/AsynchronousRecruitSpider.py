import re, asyncio, aiohttp, pymongo, time, xlrd
from lxml import html

collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['recruit_shenzhen_sales_representative']


async def crawl_recruit(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, proxy=None) as response:
            sel = html.fromstring(await response.text())
            item = {}
            for _ in sel.xpath('//div[@class="tHeader tHjob"]/div[@class="in"]/div[@class="cn"]'):
                position = _.xpath('h1/@title')
                position = ''.join(str(i) for i in position)
                location = _.xpath('span/text()')
                location = ''.join(str(i) for i in location)
                company = _.xpath('p[@class="cname"]/a/@title')
                company = ''.join(str(i) for i in company)
                industry = _.xpath('p[@class="msg ltype"]/text()')
                nature_=''.join(str(i).strip() for i in industry)
                try:
                    nature, scale, industry = re.sub(r'[\r\t\xa0 ]', '',nature_).split('|')
                except Exception as e:
                    nature, scale, industry = re.sub(r'[\r\t\xa0 ]', '',nature_).split('|'), '', ''
                item.update({'position': position, 'company': company, 'industry': industry,
                             'scale': scale, 'nature': nature,'location': location})
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
                recruit_members_release_time=','.join(str(i) for i in recruit_members_release_time)
                contact = sel.xpath('//div[@class="tCompany_main"]/div[3]/descendant::text()')
                contact = re.sub(r'[\r\t\xa0\0x80\u3000 ]', '', ''.join(str(i).strip() for i in contact))
                company_info = sel.xpath('////div[@class="tCompany_main"]/div[4]/descendant::text()')
                company_info = re.sub(r'[\r\t\xa0\u3000\0x80 ]', '', ''.join(str(i).strip() for i in company_info))
                job_description = sel.xpath('//div[@class="tCompany_main"]/div[2]/descendant::text()')
                job_description = re.sub(r'[\r\t\xa0\0x80\u3000 ]', '', ''.join(str(i).strip() for i in job_description))
                item.update({'contact': contact, 'company_info': company_info, 'job_description': job_description,
                             'recruit_members_release_time': recruit_members_release_time, 'url': url})
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
        # company_list_ = [table.row_values(rownum)[0] for rownum in range(0, 101)]
        return company_list_


def main_mongodb():
    t0 = time.time()
    # urls=parse_url('http://search.51job.com/list/020000,000000,0000,00,9,99,%25E5%2587%25BA%25E5%25B7%25AE,2,7.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=')
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
    # urls=parse_url('http://search.51job.com/list/020000,000000,0000,00,9,99,%25E5%2587%25BA%25E5%25B7%25AE,2,7.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=')
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