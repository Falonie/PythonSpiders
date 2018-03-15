import re
import time
from concurrent import futures
import requests
import pymongo
from lxml import html
from ganji_58.decorators import time_elapse, log


class GanjiTruckDrivers(object):
    def __init__(self, base_url):
        self.base_url = base_url
        self.db = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']
        self.collection = self.db['赶集_合肥']

    def generate_url(self):
        page_num = 20
        # while page_num < 21:
        while True:
            url = self.base_url.format(page_num)
            yield url
            page_num += 1

    def generate_url_yield_from(self, total):
        yield from range(1, total)

    def parse(self, url):
        r = requests.get(url).text
        selector = html.fromstring(r)
        urls = selector.xpath('//dl/dt/a/@href')
        return urls

    def drivers_details(self, url):
        r = requests.get(url).text
        selector = html.fromstring(r)
        pattern = re.compile(r'[\u3000\xa0\u2003\xae\u2022\u200b\u200c\x81\u20e3\ufe0f\xad\u202a\r\n\t ]')
        # response.encoding = 'charset=utf-8'
        driver = {}
        title = selector.xpath('//div[@class="title-line clearfix"]/h2[1]/text()')
        driver['title'] = pattern.sub('', ''.join(str(i).strip() for i in title))
        position = selector.xpath('//div[@class="title-line clearfix"]/p/text()')
        driver['position'] = pattern.sub('', ''.join(str(i).strip() for i in position))
        for _ in selector.xpath('//div[@class="module-company"]'):
            company = _.xpath('div[@class="company-info"]/h3/a/text()')
            driver['company'] = pattern.sub('', ''.join(str(i).strip() for i in company))
            driver['recruit'] = _.xpath('a[@class="position-btn"]/text()')
        for _ in selector.xpath('//div[@class="module-company"]/div[@class="information"]'):
            try:
                driver['scale'], driver['nature'], driver['industry'] = _.xpath('div[@class="introduce"]/span/text()')
            except Exception:
                driver['scale'], driver['nature'] = _.xpath('div[@class="introduce"]/span/text()')
            company_description = _.xpath('div[@class="info-text"]/div/text()')
            driver['company_description'] = pattern.sub('', ''.join(str(i).strip() for i in company_description))
        for _ in selector.xpath('//div[@class="module-basic"]'):
            location = _.xpath('div[@class="location-line clearfix"]/descendant::text()')
            driver['location'] = pattern.sub('', ''.join(str(i) for i in location))
        # authentication = selector.xpath('//div[@class="ad-firm-logo"]/div/div[last()-3]/span/text()')
        # driver['authentication'] = pattern.sub('',''.join([str(i).strip() for i in authentication]))
        # credit_ranking = selector.xpath('//div[@class="ad-firm-logo"]/div/div[last()-4]/div/@class')
        # driver['credit_ranking'] = pattern.sub('',''.join([str(i).strip() for i in credit_ranking]))
        job_description = selector.xpath('//div[@class="module-description"]/descendant::text()')
        driver['job_description'] = pattern.sub('', ''.join(str(i).strip() for i in job_description))
        driver['url'] = url
        return driver

    @log('****')
    @time_elapse('...')
    def run(self):
        for url in self.generate_url():
            print(url)
            with futures.ThreadPoolExecutor() as executor:
                urls = self.parse(url)
                if urls:
                    jobs = list(executor.map(self.drivers_details, urls, chunksize=3))
                    for number, _ in enumerate(jobs, 1):
                        print(number, _)
                    else:
                        self.collection.insert_many(jobs)
                        return len(jobs)
                elif not urls:
                    break
            time.sleep(20)

    @log('****')
    @time_elapse('....')
    def run_yield_from(self, **kwargs):
    # def run_yield_from(self, base_url, total):
        total = kwargs.get('total')
        base_url = kwargs.setdefault('base_url')
        for u in self.generate_url_yield_from(total):
            url = base_url.format(u)
            print(url)
            with futures.ThreadPoolExecutor() as executor:
                urls = self.parse(url)
                if urls:
                    jobs = list(executor.map(self.drivers_details, urls, chunksize=3))
                    for number, _ in enumerate(jobs, 1):
                        print(number, _)
                    else:
                        self.collection.insert_many(jobs)
                elif not urls:
                    break
            time.sleep(20)


if __name__ == '__main__':
    BASE_URL = 'http://hf.ganji.com/zphuoyunsiji/o{}/'
    ganji = GanjiTruckDrivers(BASE_URL)
    # print(ganji.run())
    print(ganji.run_yield_from(total=4, base_url=BASE_URL))