import scrapy

class WubaTruckDrivers(scrapy.Spider):

    name = 'wuba_truck_drivers'
    start_urls=['http://sh.58.com/sonhuosiji/?PGTID=0d303668-0000-2729-3bbd-759ea9bb0785&ClickID=2']

    def parse(self, response):
        for href in response.xpath('//div[@id="infolist"]/dl/dt/a/text()').extract():
            yield {'href':href}