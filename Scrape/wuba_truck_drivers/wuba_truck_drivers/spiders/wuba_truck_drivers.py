import scrapy

class WubaTruckDrivers(scrapy.Spider):

    name = 'wuba_truck_drivers'
    start_urls=['http://sh.58.com/sonhuosiji/pn{page}/?PGTID=0d302517-0000-2758-37fc-c2a3b0f3231b&ClickID=4']

    def start_requests(self):
        for i in range(1, 9):
            url = self.start_urls[0].format(page=i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.xpath('//div[@id="infolist"]/dl/dt'):
            # yield {'title':item.xpath('a/text()').extract_first(),
            #        'href':item.xpath('a/@href').extract_first()}
            yield scrapy.Request(url=item.xpath('a/text()').extract_first(), callback=self.driver_details)

    def driver_details(self,response):
        yield {''}
