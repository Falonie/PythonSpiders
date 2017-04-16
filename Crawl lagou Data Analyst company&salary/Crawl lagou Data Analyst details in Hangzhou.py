import requests,re
from bs4 import BeautifulSoup
from lxml import html

baseurl = 'https://www.lagou.com/zhaopin/shujufenxishi/{}/?filterOption=2'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
cookie = {
    'Cookie': 'user_trace_token=20170326001734-ec41389ced6b4a4882609bf9e467bdb2; LGUID=20170326001734-8e3315f4-1176-11e7-9569-5254005c3644; JSESSIONID=197AA9B8333FB8CB7DF60C237916266D; _putrc=43700CED3E324D1B; login=true; unick=%E7%8E%8B%E6%99%B4%E6%99%A8; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=8; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_navigation; SEARCH_ID=47ef26b4046945ae8677be130dd18a7a; index_location_city=%E6%9D%AD%E5%B7%9E; _gat=1; _ga=GA1.2.1946463376.1490458642; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1490458642,1491055889; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1492262327; LGSID=20170415210122-9fdb72b0-21db-11e7-a32c-5254005c3644; LGRID=20170415211900-1697c1a5-21de-11e7-b5fa-525400f775ce'}

def lagou_hangzhou():
    for i in range(1,31):
        session = requests.session()
        url=baseurl.format(i)
        response = session.get(url, headers=header, cookies=cookie).text
        bsobj = BeautifulSoup(response, 'html.parser')
        sel = html.fromstring(response)
        company_name = sel.xpath('//div[@class="company_name"]/a/text()')
        block = sel.xpath('//div[@class="p_top"]/a/span/em/text()')
        salary = sel.xpath('//span[@class="money"]/text()')
        experience = re.findall(r'<!--<i></i>-->(.*?)/', str(bsobj))
        industry=sel.xpath('//div[@class="industry"]/text()')
        # bsobj = bsobj.findAll("div", class_="industry")
        # for i in bsobj:
        #     print(i.contents[0].strip().split('/')[0])
        for c, s, e, b, i in zip(company_name, salary, experience, block, industry):
            print(c, s, e, b, i.strip().split('/')[0])

if __name__=='__main__':
    lagou_hangzhou()