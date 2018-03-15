import re
import time
from concurrent import futures
import requests
import pymongo
from lxml import html

BASE_URL = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=%E9%94%80%E5%94%AE&isadv=0&sg=d1adcdbd993b45148ae48fe7e01806e0&p={}'
BASE_URL2 = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E6%B7%B1%E5%9C%B3&kw=python&isadv=0&sg=2ea8e822600943f5921b1e5846720832&p={}'
collection = pymongo.MongoClient(host='127.0.0.1', port=27017)['Falonie']['recruit_test']


class Recruit(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def generate_url(self):
        for page_num in range(42, 91):
            url = self.base_url.format(page_num)
            yield url

    def parse(self, url):
        r = requests.get(url).text
        pattern5 = re.compile(r'<a style="font-weight:.*?href="(.*?)" target="_blank">')
        href = pattern5.findall(r)
        return href

    def parse_page(self, url):
        r = requests.get(url).text
        selector = html.fromstring(r)
        recruit = {}
        pattern = re.compile(r'[\xa0\n\r\t ]')
        for _ in selector.xpath('//div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]'):
            job_description = _.xpath('div[1]/descendant::text()')
            job_description = pattern.sub('', ''.join(str(i).strip() for i in job_description))
            company_description_ = _.xpath('div[2]/descendant::text()')
            company_description = pattern.sub('', ''.join(str(i).strip() for i in company_description_))
            recruit['job_description'] = job_description
            recruit['company_description'] = company_description
        for i in selector.xpath('//div[@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li'):
            a = i.xpath('span/text()')
            a = ''.join(str(i) for i in a)
            b = i.xpath('strong/text()|strong/a/text()|strong/span/text()')
            b1 = pattern.sub('', ''.join(str(i) for i in b))
            recruit[a] = b1
        for _ in selector.xpath('//div[@class="company-box"]/ul/li'):
            a = _.xpath('span/text()')[0]
            b = _.xpath('strong/descendant::text()')
            b = ''.join(str(i).strip() for i in b)
            recruit[a] = b
        company_name = selector.xpath('//p[@class="company-name-t"]/a/text()')
        recruit['company_name'] = ''.join(str(i) for i in company_name)
        position = selector.xpath('//div[@class="fixed-inner-box"]/div[1]/h1/text()')
        recruit['position'] = ''.join(str(i) for i in position)
        recruit['url'] = url
        return recruit

    def main(self):
        for url in self.generate_url():
            print(url)
            with futures.ThreadPoolExecutor() as executor:
                urls = self.parse(url)
                if urls:
                    jobs = list(executor.map(self.parse_page, urls))
                    for number, _ in enumerate(jobs, 1):
                        print(number, _)
                    else:
                        collection.insert_many(jobs)
                else:
                    break
                time.sleep(10)


if __name__ == '__main__':
    recruit = Recruit(BASE_URL2)
    recruit.main()