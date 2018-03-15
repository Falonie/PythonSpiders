import re
import time
from concurrent import futures
import requests
import pymongo
from lxml import html
from ganji_58.decorators import time_elapse, log


class WubaRecruit(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.db = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']
        self.collection = self.db['58_淮南']

    def generate_url(self):
        page_num = 3
        # while page_num < 7:
        while True:
            url = self.base_url.format(page_num)
            yield url
            page_num += 1

    def parse(self, url):
        r = requests.get(url).text
        selector = html.fromstring(r)
        href_list = selector.xpath('//div[@class="item_con job_title"]/div[@class="job_name clearfix"]/a/@href')
        return href_list

    def driver_details(self, url):
        r = requests.get(url).text
        selector = html.fromstring(r)
        pattern = re.compile(r'[\u3000\xa0\u2003\xae\u2022\u200b\u200c\x81\u20e3\ufe0f\xad\u202a\u200d\u2212\r\t\n ]')
        driver = {}
        for item in selector.xpath('//div[@class="item_con pos_info"]'):
            title = item.xpath('div[@class="pos_base_info"]/span/text()')
            driver['title'] = ''.join([str(i) for i in title])
            driver['position'] = ''.join([str(i) for i in item.xpath('span/text()')])
            recruit = item.xpath(
                'div[@class="pos_base_condition"]/span[@class="item_condition pad_left_none"]/text()')
            driver['recruit'] = ''.join([str(i) for i in recruit])
            location = item.xpath('div[@class="pos-area"]/span/descendant::text()')
            driver['location'] = ''.join([str(i).strip().replace('查看地图', '') for i in location])
            company = selector.xpath(
                '//div[@class="comp_baseInfo_title"]/div[@class="baseInfo_link"]/a/text()')
            driver['company'] = ''.join([str(i) for i in company])
            industry = selector.xpath('//p[@class="comp_baseInfo_belong"]/a/text()')
            driver['industry'] = ''.join([str(i) for i in industry])
            scale = selector.xpath('//p[@class="comp_baseInfo_scale"]/text()')
            driver['scale'] = ''.join([str(i) for i in scale])
            job_description = selector.xpath(
                '//div[@class="item_con"]/div[1]/div[@class="posDes"]/div[@class="des"]/text()')
            driver['job_description'] = pattern.sub('', ''.join([str(i).strip() for i in job_description]))
            company_description = selector.xpath('//div[@class="intro"]/div/p/text()')
            driver['company_description'] = pattern.sub('', ''.join([str(i).strip() for i in company_description]))
            driver['url'] = url
        return driver

    @log('****')
    @time_elapse('....')
    def main(self):
        for url in self.generate_url():
            print(url)
            with futures.ThreadPoolExecutor() as executor:
                urls = self.parse(url)
                if urls:
                    jobs = list(executor.map(self.driver_details, urls, chunksize=3))
                    for number, _ in enumerate(jobs, 1):
                        print(number, _)
                    else:
                        self.collection.insert_many(jobs)
                elif not urls:
                    break
                time.sleep(20)


if __name__ == '__main__':
    BASE_URL = 'http://hn.58.com/sonhuosiji/pn{}/?PGTID=0d302517-0090-fdcd-64a7-5788cf5b9669&ClickID=3'
    wuba = WubaRecruit(BASE_URL)
    wuba.main()