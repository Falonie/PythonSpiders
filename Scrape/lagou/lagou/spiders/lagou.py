import scrapy
from ..items import LagouItem
from scrapy.http import Request

class Lagou(scrapy.Spider):
    name = "lagou"
    #start_urls = ['https://www.lagou.com/zhaopin/Python/3/?filterOption=3']
    start_urls = 'https://www.lagou.com/zhaopin/shujufenxishi/{}/?filterOption=2'

    def start_requests(self):
        # header = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        # cookie = {
        #     'Cookie': 'user_trace_token=20170430161023-840993cb5bb440338eba98041a89066a; LGUID=20170430161024-763ed5c6-2d7c-11e7-8952-525400f775ce; JSESSIONID=A9FCDAFD6FED735C2957B02698D8E1A2; _putrc=43700CED3E324D1B; login=true; unick=%E7%8E%8B%E6%99%B4%E6%99%A8; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=36; TG-TRACK-CODE=index_navigation; SEARCH_ID=f5c542f21a7d4623a045741c19582b33; index_location_city=%E6%9D%AD%E5%B7%9E; _gat=1; _ga=GA1.2.742080781.1493539778; _gid=GA1.2.44052745.1493883245; LGSID=20170504150457-fbb34bfd-3097-11e7-b572-5254005c3644; LGRID=20170504153459-2d471c6a-309c-11e7-b572-5254005c3644; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1493539782; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1493883245'}
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        cookie = {
            'Cookie': 'user_trace_token=20170326001734-ec41389ced6b4a4882609bf9e467bdb2; LGUID=20170326001734-8e3315f4-1176-11e7-9569-5254005c3644; JSESSIONID=197AA9B8333FB8CB7DF60C237916266D; _putrc=43700CED3E324D1B; login=true; unick=%E7%8E%8B%E6%99%B4%E6%99%A8; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=8; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_navigation; SEARCH_ID=47ef26b4046945ae8677be130dd18a7a; index_location_city=%E6%9D%AD%E5%B7%9E; _gat=1; _ga=GA1.2.1946463376.1490458642; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1490458642,1491055889; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1492262327; LGSID=20170415210122-9fdb72b0-21db-11e7-a32c-5254005c3644; LGRID=20170415211900-1697c1a5-21de-11e7-b5fa-525400f775ce'}

        for i in range(1, 5):
            url = self.start_urls.format(i)
            yield scrapy.Request(url=url, headers=header, cookies=cookie,method='GET', callback=self.parse)

    def parse(self, response):
        #print(response)
        lagou = LagouItem()
        salary = response.xpath('.//div[@class="li_b_l"]/span[@class="money"]/text()').extract()
        company_name = response.xpath('.//div[@class="company_name"]/a/text()').extract()
        block = response.xpath('//div[@class="p_top"]/a/span/em/text()').extract()
        # industry = response.xpath('//div[@class="industry"]/text()').strip().extract()
        for s, c, b in zip(salary, company_name, block):
            lagou['salary'] = s
            lagou['company_name'] = c
            lagou['block'] = b
            yield lagou
            # print(s, c, b)
            # yield scrapy.Request()
