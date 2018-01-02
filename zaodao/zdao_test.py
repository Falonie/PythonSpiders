import requests,re,asyncio,aiohttp
from lxml import html
from multiprocessing import Pool

url='https://www.zdao.com/info/searchPerson'
headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'}
cookies={'Cookie':'JSESSID=7qi5fr46l2phjodqf70e2377g6; _cpcl=5a2116df5186e; S2=DF0CD3BD7A904EA1C8APY9MK; Hm_lvt_dd717aa780606579d5c95d7bf64d529c=1512117988,1512379729; Hm_lpvt_dd717aa780606579d5c95d7bf64d529c=1512442030'}
data={'keyword':'创始人','start':'40','city':'3301','pageSize':'20','YII_CSRF_TOKEN':'2beed4c38c204f4335b32b65d22736db'}
def parse_page_details(url):
    r = requests.get(url=url, headers=headers, cookies=cookies).text
    selector = html.fromstring(r)
    # 修改写入数据库表名
    collection = db['zdao_创始人_personal_information']
    for _ in selector.xpath('//div[@class="user_career"]'):
        user_name = ''.join(str(i).strip() for i in _.xpath('p[@class="user_name"]/text()'))
        user_title = ''.join(str(i).strip() for i in _.xpath('p[@class="user_title"]/text()'))
        user_company = ''.join(str(i).strip() for i in _.xpath('a[@class="user_company"]/text()'))
        business = ''.join(str(i).strip() for i in _.xpath('p[@class="business"]/text()'))
        small_title = ''.join(str(i).strip() for i in
                              selector.xpath('//a[@data-stat-key="my_company_info"]/div[@class="small_title"]/text()'))
        establish_time = ''.join(
            str(i).strip() for i in selector.xpath('//a[@data-stat-key="my_company_info"]/div[3]/text()'))
        establish_time = re.sub(r'[\xa0\t ]', '', establish_time)
        # print(small_title,establish_time)
        # ''.join(str(i).strip() for i in )
        # for _ in selector.xpath('//div[@class="half_item border_bottom"]'):
        eduction = ''.join(str(i).strip() for i in selector.xpath(
            '//div[@class="half_item border_bottom"]/div[@class="small_title"]/div/text()'))
        faculty = ''.join(str(i).strip() for i in selector.xpath(
            '//div[@class="half_item border_bottom"]/div[@class="half_item_info_wrapper"]/div/text()'))
        eduction_time = ''.join(str(i).strip() for i in selector.xpath(
            '//div[@class="half_item border_bottom"]/div[@class="half_item_info education_time"]/text()'))
        mobile = selector.xpath('//*[@class="item_info mobile_item"]/text()')
        mobile = ''.join(str(i).strip() for i in mobile)
        email = ''.join(str(i).strip() for i in selector.xpath('//a[@class="item_info mail_item contact_item"]/text()'))
        qq = ''.join(str(i).strip() for i in selector.xpath('//div[@class="item_info QQ_item contact_item"]/text()'))
        weixin = ''.join(
            str(i).strip() for i in selector.xpath('//div[@class="item_info weixin_item contact_item"]/text()'))
        gender = ''.join(str(i).strip() for i in selector.xpath('//div[@class="item_info gender"]/text()'))
        industry = ''.join(str(i).strip() for i in selector.xpath('//div[@class="item_info industry_name"]/text()'))
        location = ''.join(str(i).strip() for i in selector.xpath('//div[@class="item_info town_code"]/text()'))
        user = {'user_name': user_name, 'user_title': user_title, 'user_company': user_company, 'business': business,
                'small_title': small_title, 'establish_time': establish_time, 'eduction': eduction, 'faculty': faculty,
                'eduction_time': eduction_time, 'mobile': mobile, 'email': email, 'qq': qq, 'weixin': weixin,
                'industry': industry, 'location': location}
        collection.insert_one(user)
        return user
