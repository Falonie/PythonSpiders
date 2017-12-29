import requests, re
from lxml import html

# url='http://search.51job.com/list/020000,000000,0000,00,9,99,%25E5%2587%25BA%25E5%25B7%25AE,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
url = 'http://search.51job.com/list/020000,000000,0000,00,9,99,%25E5%2587%25BA%25E5%25B7%25AE,2,3.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
session = requests.session()


def parse_url(url):
    r = session.get(url).text
    selector = html.fromstring(r)
    urls = []
    # for _ in selector.xpath('//div[@id="resultList"]/div[@class="el"]'):
    #     href = _.xpath('p/span/a/@href')[0]
    #     title = _.xpath('p/span/a/@title')[0]
    #     urls.append(href)
    urls = [{'url': _} for _ in selector.xpath('//div[@id="resultList"]/div[@class="el"]/p/span/a/@href')]
    return urls


def parse_page(url):
    r = session.get(url=url)
    r.encoding = 'gb2312'
    sel = html.fromstring(r.text)
    item = {}
    for _ in sel.xpath('//div[@class="tHeader tHjob"]/div[@class="in"]/div[@class="cn"]'):
        position = _.xpath('h1/@title')
        position = ''.join(str(i) for i in position)
        location = _.xpath('span/text()')
        location = ''.join(str(i) for i in location)
        company = _.xpath('p[@class="cname"]/a/@title')
        company = ''.join(str(i) for i in company)
        industry = _.xpath('p[@class="msg ltype"]/text()')
        nature_ = ''.join(str(i).strip() for i in industry)
        try:
            nature, scale, industry = re.sub(r'[\r\t\xa0 ]', '', nature_).split('|')
        except Exception as e:
            nature, scale, industry = re.sub(r'[\r\t\xa0 ]', '', nature_).split('|'), '', ''
        item.update({'position': position, 'company': company, 'industry': industry, 'scale': scale, 'nature': nature,
                     'location': location})
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
        contact = sel.xpath('//div[@class="tCompany_main"]/div[3]/descendant::text()')
        contact = re.sub(r'[\r\t\xa0 ]', '', ''.join(str(i).strip() for i in contact))
        company_info = sel.xpath('//div[@class="tCompany_main"]/div[4]/descendant::text()')
        company_info = re.sub(r'[\r\t\xa0 ]', '', ''.join(str(i).strip() for i in company_info))
        job_description = sel.xpath('//div[@class="tCompany_main"]/div[2]/descendant::text()')
        job_description = re.sub(r'[\r\t\xa0 ]', '', ''.join(str(i).strip() for i in job_description))
        item.update({'contact': contact, 'company_info': company_info, 'job_description': job_description,
                     'recruit_members_release_time': recruit_members_release_time, 'url': url})
    return item


if __name__ == '__main__':
    print(parse_page(url='http://jobs.51job.com/guangzhou-thq/81574774.html?s=01&t=0'))
    print('招6人'.startswith('招'))
    for i in ['1年经验', '高中', '招6人', '12-26发布']:
        # print(i)
        recruit_members_ = i if str(i).endswith('人') else ''
        # if str(i).endswith('人'):
        #     recruit_members_=i
        print(recruit_members_)
    # print(parse_url(
    #     'http://search.51job.com/list/020000,000000,0000,00,9,99,%25E5%2587%25BA%25E5%25B7%25AE,2,7.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='))