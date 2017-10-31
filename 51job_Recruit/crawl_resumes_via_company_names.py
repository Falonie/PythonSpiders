import requests, re, time, pymongo, logging, random
from lxml import html
from multiprocessing import Pool

collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie']['Cloud_bird_Recruit_51Job_Resume_Tianjin']
url = 'https://ehire.51job.com/Candidate/SearchResumeNew.aspx'
headers = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
]
# headers = {
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
cookies = {
    'Cookie': '51job=cenglish%3D0%26%7C%26; guid=15094380488800880010; EhireGuid=96a5be8e83bb470a8e475ef5e6f579e7; ASP.NET_SessionId=1a25fyvwbgk4xyjust2agdvt; HRUSERINFO=CtmID=2585839&DBID=3&MType=02&HRUID=2965014&UserAUTHORITY=1100111011&IsCtmLevle=1&UserName=%e8%b6%85%e4%b9%90%e5%81%a5%e5%ba%b7&IsStandard=0&LoginTime=10%2f31%2f2017+16%3a22%3a12&ExpireTime=10%2f31%2f2017+16%3a32%3a12&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=2&AccessKey=e83546cdfa9498f0; AccessKey=f333c1a70504471; RememberLoginInfo=member_name=E2BF04DB6CCD2D50FAD638DD50DCF144&user_name=E2BF04DB6CCD2D50FAD638DD50DCF144; LangType=Lang=&Flag=1; KWD=SEARCH=%25e7%2589%25a9%25e6%25b5%2581%2b%25e8%25bf%2590%25e8%25be%2593%2b%25e6%258b%259b%25e6%25a0%2587%2b%25e4%25be%259b%25e5%25ba%2594%25e9%2593%25be%2b'}
data = {
    '__EVENTTARGET': 'ctrlSerach$search_submit',
    '__VIEWSTATE': '/wEPDwUJODA0MTA0NTMxDxYOHgRJc0VOaB4QdnNTZWxlY3RlZEZpZWxkcwUzQUdFLFdPUktZRUFSLFNFWCxBUkVBLFdPUktGVU5DLFRPUERFR1JFRSxMQVNUVVBEQVRFHghQYWdlU2l6ZQIyHgxzdHJTZWxlY3RDb2wFM0FHRSxXT1JLWUVBUixTRVgsQVJFQSxXT1JLRlVOQyxUT1BERUdSRUUsTEFTVFVQREFURR4JUGFnZUluZGV4AhAeCFBhZ2VEYXRhBbQQODAxfDEwMDB8MjAwfDE2NjZ8NzIxNTg0MTMsNTQ4NDgyLDI2MDA1MzI2LDM2NDA0OTQxOSwzNDYwNjMzMjUsMzk1MzI1MiwzNDQ5ODIxODYsOTIwNTE1OTEsMzU5ODMzMDMyLDQxNDQ3MzIsMjYwMjUzNzMsMTQ5MjgwODcsMTM3NzM2MTEsNjIwNTYxNzQsMzIwNjU3MDEzLDI4NDE1MTc5LDM1MDk2MTcyMCw3ODg0OTEsMzU3MjM4NTM2LDMyMDcyMzcwNiw1MTYwOTQzNSwzNjQxMTQ4MzksNTI4ODY0NjcsMzYwNzI2NzE0LDM2MzMyOTAwOCwyNDI4MDg5NiwzNTU2Mjk4ODIsNDA4ODU1NiwzMjgyNjg1MDQsMzQ1OTM1ODc1LDMyNTQ3Mjk1NSw2NzY3NTk0MSwzNTc3Njc5ODYsODUzMTkwOCw5MDY5NDA4MSwzNjM4NDY1MzIsNjQ2NzUzMiwxMzE5ODk1NSwyNzUxNzg3NSwxOTAzNTc3NiwzNjQxMTg1ODIsNjY4MjY2OSwzNTM2OTU0NDUsODA0Nzk1LDU0Mzg2NzU2LDMyNDE1ODEwLDMzODkyMjQ3NSw4MjIyODg2MiwxNzQwODM1MCwzNTc0NzIxOTAsMzU2NjA1MDAxLDExOTM5MzQzLDMxMzExOTM2MSw4NTAzNzA2MiwyOTY4Njc4LDM2MjcyODA0NiwxNTA1MjU1Niw1ODUzMDQxOSw2MzQ1Mzg5LDExMTk3MjAxLDMxOTc0MzEwMywzNjM5ODUzMzgsNjI3MTk4NzUsMzA4NzY5MDA0LDM0OTYzNTA1MCwzMTk1MjIwMTEsMjUzMzI5MTAsMzUyNDI0MTc2LDY0NTMyNDk2LDcyODU3MzI1LDM1NDM3OTQxOCwyOTE3MzQ1NiwzNjM3OTAxMTYsNTUxMDIwLDM1NDk4NDU0MywzMTE3MzU2OTMsMzYyMDE2MTYyLDMyMjUzMTcxNSwzMzk1NjI0MzksMjcyNzE5MjIsNzYyODI1MjMsMzIxNzgwMjU5LDk1MDQ5NDAsMzUwOTE0MzkyLDM2MzcxODA4Niw3NTYyNzIyMSw1ODgyMjIxLDMxOTQ1Nzc5LDIzNzQ4ODIsMzYzMzEyODgwLDc3NzAwNTcyLDMxNzY2ODQsMzA5MjEyMDA2LDM1NjQyMzQ3NCwzNjI2OTU2NzQsMzQ4NjgzMzIxLDM2MDcwNjYwMyw1NTM4NDcwLDE0OTc5NjgzLDI3MTc3MTIxLDY2NjI3NjI1LDQ0OTM4ODEsNTgzMTM4NTcsMzU0NzgwNjk2LDE0MTk2OTM4LDM2MTUxMjMzNiw1MzkyMTIwNCwzNjMyNTc4MjgsMTI0MDI0Niw1MzgzNDYwNSwzMTMzMDY5Myw3ODM2MTA2OSw5MDk5MDQ4LDM2MjkwMjkxOCwzNjMyOTgxNTYsMzYyNDE2ODI4LDcyMDQ2MzgxLDgxNzc3NzIxLDkzNjQ3MDUsODAxNDkyNjgsMTIzODg0Miw1NTE5NzM3LDE4MjI3NzY4LDM2MTU4NTAzNiwxNDQzNTQ0NCwzMjQzNTc5NzQsODE3MjU0NDQsNTEwMDE1MDYsMzQ5Mzc2NTA3LDc1MzI5NjM5LDMxNzEwNjgzOCw1MTM4MjYsMzIxMDc4MzQzLDk2MDA5MDQsMzA0Njc5NDY4LDMxNTAyODM2NCwzMTQyOTQyNzgsOTYxMjU5NTEsMjUzMjU4MDYsMzYwNDE0ODE2LDg0MTIzMjM1LDU4MjgwOTE0LDMxNjE4MzMzLDM1OTIwMDE2Nyw0OTU3MDA1NCwzMDcxMzA2NDcsOTAxMTQ5MjMsNTA1MTIyNzcsMzU4NjIzMDYzLDYzOTg0NDAyLDM1OTUzMzA4NSwzNTEyNjk3NTYsMTA3MzY0NjMsMzU5NDIzOTMzLDM0NDIwNTM3NCw2ODAzODIwLDM2MjU3MDUzNSw0OTQwMTE3OSwzMTI4NTE5NDcsMzYwNDM2NDQwLDM1NDM3MzAyMCwzNTg0MTEzMjYsMzYxNzkxMDQ0LDM1NjkxMTM0NiwzMjA0NDIwMTksODk4OTU3OTEsMzYyMjk2MjA3LDY0Mjg2NDExLDcwNTM3MTQ2LDM0NjA1NDEwNywxNjQyODAxMywxMDkyNzU5MCwzNjAwNzY3NjYsMTM0MjQxMSw3NjE0MDE2Myw2MTgyMzM1MCwyNjkxNzAwNywzMDgzMjYyOTMsNTE3NTE4NDYsNzAwOTAxOTcsMTU5MTUwMDYsNjgxMjM4MTMsMzYyNDM0NTU0LDQ4NjM2MCwzMzMzNjQ1MTMsMzI1MjM3MzAwLDY5NjA3MDcsNjc4OTA5NjIsMzM0Mjg2NzkwLDg5MjI0MTIyLDM5ODI4ODYsMzYwMjUyMTMxLDM2MjI3NTA5NiwzNjE1MTgwNzUsMzU3NDYzNjA1LDM1NTIxNzg5MiwzNDM2NTA3OTUsNzE4Nzg2NCwzNjIyMDk5MTgsNjQ5NjQ2MTB8TUNNd0l6QWpPWHd3TVRBd01EQXdNakF3TURBd05UQXdNREI4TURneU56QTRNamd3T0RJMWZEQXdmREF3ZkRBd01EQjhNakF4TmpFd016RjhNakF4TnpFd016RjhNREF3TURBd01EQjhNREF3TURBd01EQjhNSHc1ZkRCOE1Id3dmREI4TURBd01Id3dNREF3ZkRCOE1IeDhmREI4TUh3NWZEbDhPWHc1ZkRsOE9Yd3dNREF3TURCOE1EQXdNSHd3TURBd2ZEQXdNREF3TUh3eGZEbDhPREF4SXpFd01EQWpFQkFRHgxUb3RhbFJlY29yZHMCgg0WAgIBD2QWGAICDw8WBB4RSXNDb3JyZWxhdGlvblNvcnQFATAeCElzVXNlcklEBQEwZGQCBQ9kFgJmDxAPFgIeB0NoZWNrZWRoZGRkZAIGDw8WBB4IQ3NzQ2xhc3MFF1NlYXJjaF9yZXN1bWVfYnV0dG9uX29uHgRfIVNCAgJkZAIHDw8WBB8KBSZDb21tb25faWNvbiBTZWFyY2hfYnRuX2xhYmVsX2Fycm93X0Nvch8LAgJkZAIIDw8WBB8KBRlTZWFyY2hfcmVzdW1lX2J1dHRvbl9vdXQyHwsCAmRkAgkPDxYEHwoFFFNlYXJjaF9idG5fbGFibGVfbm9uHwsCAmRkAgoPDxYCHgRUZXh0BQrlhbExNjY25p2hZGQCCw8PFgQfCgUqQ29tbW9uX2ljb24gU2VhcmNoX3Jlc3VtZV9idXR0b25fZGlzaW1nX29uHwsCAmRkAgwPDxYEHwoFLENvbW1vbl9pY29uIFNlYXJjaF9yZXN1bWVfYnV0dG9uX2Rpc2ltZ19kb3V0HwsCAmRkAg0PDxYIHwBoHgpQUGFnZUluZGV4AhAfAgIyHwYCgg1kFgICAg8QZGQWAQICZAIODw8WCB8AaB8NAhAfAgIyHwYCgg1kFhACAQ8PFgofDAUCMTUeD0NvbW1hbmRBcmd1bWVudAUCMTUeB1Rvb2xUaXAFAjE1HwplHwsCAmRkAgIPDxYKHwwFAjE2Hw4FAjE2Hw8FAjE2HwplHwsCAmRkAgMPDxYKHwwFAjE3Hw4FAjE3Hw8FAjE3HwoFBmFjdGl2ZR8LAgJkZAIEDw8WCh8MBQIxOB8OBQIxOB8PBQIxOB8KZR8LAgJkZAIFDw8WCh8MBQIxOR8OBQIxOR8PBQIxOR8KZR8LAgJkZAIGDw8WAh8MBQMuLi5kZAIHDw8WAh8MBQMuLi5kZAIIDw8WBh8PBQIzNB8MBQIzNB8OBQIzNGRkAg8PEGQQFQ0G5bm06b6EDOW3peS9nOW5tOmZkAbmgKfliKsJ5bGF5L2P5ZywBuiBjOiDvQblrabljoYS566A5Y6G5pu05paw5pe26Ze0BuaIt+WPowzmnJ/mnJvmnIjolqoM55uu5YmN5pyI6JaqBuihjOS4mgbkuJPkuJoJ5a2m5qCh5ZCNFQ0DQUdFCFdPUktZRUFSA1NFWARBUkVBCFdPUktGVU5DCVRPUERFR1JFRQpMQVNUVVBEQVRFBUhVS09VDEVYUEVDVFNBTEFSWQ1DVVJSRU5UU0FMQVJZDFdPUktJTkRVU1RSWQhUT1BNQUpPUglUT1BTQ0hPT0wUKwMNZ2dnZ2dnZ2dnZ2dnZ2RkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYQBQ1jaGtIYXNQaWNfYmFrBQljaGtIYXNQaWMFDGNieENvbHVtbnMkMAUMY2J4Q29sdW1ucyQxBQxjYnhDb2x1bW5zJDIFDGNieENvbHVtbnMkMwUMY2J4Q29sdW1ucyQ0BQxjYnhDb2x1bW5zJDUFDGNieENvbHVtbnMkNgUMY2J4Q29sdW1ucyQ3BQxjYnhDb2x1bW5zJDgFDGNieENvbHVtbnMkOQUNY2J4Q29sdW1ucyQxMAUNY2J4Q29sdW1ucyQxMQUNY2J4Q29sdW1ucyQxMgUNY2J4Q29sdW1ucyQxMg==',
}
search_value = '物流 or 运输 or 招标 or 供应链#北京|010000$上海|020000$天津|050000#0#########{}###########近1年|6##1#1###0#0#0'
response = requests.post(url=url, data=data, headers={'User-Agent': random.choice(headers)}, cookies=cookies).text
selector = html.fromstring(response)
def generate_response():
    with open('/media/salesmind/Other/cloud_bird/库-云鸟（10.27）.txt', 'r') as f:
        for i, line in enumerate(f.readlines(), 1):
            # print(i,line.strip())
            # yield search_value.format(line.strip())
            data.update({'ctrlSerach$hidSearchValue': search_value.format(line.strip())})
            # print(i,j.strip())
            # print(i,data)
            response = requests.post(url=url, data=data, headers={'User-Agent': random.choice(headers)},
                                     cookies=cookies).text
            # selector = html.fromstring(response)
            yield response


def urls(r):
    try:
        selector = html.fromstring(r)
        url_list = []
        for i in selector.xpath('//div[@class="Common_list-table"]/table/tbody/tr[@class="inbox_tr1"]|'
                                '//div[@class="Common_list-table"]/table/tbody/tr[@class="inbox_tr2"]'):
            href = i.xpath('td[@class="Common_list_table-id-text"]/span/a/@href')[0]
            ID = i.xpath('td[@class="Common_list_table-id-text"]/span/a/text()')[0]
            # print(ID, 'http://ehire.51job.com/{}'.format(href))
            url_list.append('http://ehire.51job.com/{}'.format(href))
        return url_list
    except:
        pass


def parse_url(url):
    response = requests.get(url=url, headers={'User-Agent': random.choice(headers)}, cookies=cookies).text
    sel = html.fromstring(response)
    try:
        a = sel.xpath(
            '//*[@id="divInfo"]/td/table[4]/tr[2]/td/table/tr[1]/td/table/tbody/tr[1]/td[2]/span[1]/text()')[0]
        for i in sel.xpath('//*[@id="divInfo"]/td/table[4]/tr[2]/td/table/tr[1]'):
            update_time = sel.xpath('//*[@id="lblResumeUpdateTime"]/descendant::text()')
            update_time = ''.join(str(i).strip() for i in update_time)
            time = i.xpath('td/table/tbody/tr[1]/td[1]/text()')[0]
            company = i.xpath('td/table/tbody/tr[1]/td[2]/span[1]/text()')[0]
            company = re.sub(r'[#→star←end]', '', str(company))
            period = ''.join(str(i).strip() for i in i.xpath('td/table/tbody/tr[1]/td[2]/span[2]/text()'))
            period = re.sub(r'[\n ]', '', period)
            try:
                industry = i.xpath('td/table/tbody/tr[2]/td[2]/descendant::text()')[0]
                industry = re.sub(r'[#→star←end]', '', str(industry))
            except:
                industry = 'N/A'
            # industry = re.sub(r'[#→star←end]', '', industry)
            text = i.xpath('td/table/tbody/tr[2]/td[2]/descendant::text()')
            try:
                scale = text[2]
            except Exception as e:
                scale = ''
            try:
                nature = text[4]
            except Exception as e:
                nature = ''
            position = i.xpath('td/table/tbody/tr[3]/descendant::text()')
            position = re.sub(r'[#→star←end]', '', ''.join(str(i).strip() for i in position))
            description = ''.join(
                str(i).strip() for i in i.xpath('td/table/tbody/tr[4]/descendant::text()'))
            # print(a, company, period, industry, description)
            description = re.sub(r'[#→star←end ]', '', description)
            ID = re.findall('<title>\s*(.*?)\s*</title>', response)[0]
            return {'ID': ID, 'update_time': update_time, 'time': time, 'company': company, 'period': period,
                    'industry': industry, 'scale': scale, 'nature': nature, 'position': position,
                    'description': description}
    except:
        for i in sel.xpath('//*[@id="divInfo"]/td/table[3]/tr[2]/td/table/tr[1]'):
            update_time = sel.xpath('//*[@id="lblResumeUpdateTime"]/descendant::text()')
            update_time = ''.join(str(i).strip() for i in update_time)
            try:
                time = i.xpath('td/table/tbody/tr[1]/td[1]/text()')[0]
            except:
                time = 'N/A'
            try:
                company = i.xpath('td/table/tbody/tr[1]/td[2]/span[1]/text()')[0]
                company = re.sub(r'[#→star←end]', '', str(company))
            except:
                company = 'N/A'
            period = ''.join(str(i).strip() for i in i.xpath('td/table/tbody/tr[1]/td[2]/span[2]/text()'))
            period = re.sub(r'[\n ]', '', period)
            try:
                industry = i.xpath('td/table/tbody/tr[2]/td[2]/descendant::text()')[0]
                industry = re.sub(r'[#→star←end]', '', str(industry))
            except:
                industry = 'N/A'
            # industry = re.sub(r'[#→star←end]', '', industry)
            # recruit['test']=i.xpath('td/table/tbody/tr[2]/td[2]/descendant::text()').extract()
            text = i.xpath('td/table/tbody/tr[2]/td[2]/descendant::text()')
            try:
                scale = text[2]
            except Exception as e:
                scale = ''
            try:
                nature = text[4]
            except Exception as e:
                nature = ''
            position = i.xpath('td/table/tbody/tr[3]/descendant::text()')
            position = re.sub(r'[#→star←end]', '', ''.join(str(i).strip() for i in position))
            description = ''.join(
                str(i).strip() for i in i.xpath('td/table/tbody/tr[4]/descendant::text()'))
            description = re.sub(r'[#→star←end ]', '', description)
            ID = re.findall('<title>\s*(.*?)\s*</title>', response)[0]
            # print(a, company, period, industry, description)
            return {'ID': ID, 'update_time': update_time, 'time': time, 'company': company, 'period': period,
                    'industry': industry, 'scale': scale, 'nature': nature, 'position': position,
                    'description': description}


def main():
    # print(urls())
    for i, j in enumerate(generate_response(), 1):
        t0 = time.time()
        if urls(j):
            print(i, type(urls(j)), urls(j))
            with Pool() as pool:
                p = pool.map(parse_url, urls(j))
                # print(p, len(p), type(p))
                for i, j in enumerate(p, 1):
                    print(i, j, type(j))
                    try:
                        collection.insert_one(j)
                    except Exception as e:
                        print(e)
        print(time.time() - t0)
        time.sleep(12)


if __name__ == '__main__':
    main()
    # print(type(generate_response()))
    # for i,j in enumerate(generate_response(),1):
    #     if urls(j):
    #         print(i,type(urls(j)),urls(j))
    # else:
    #     pass
    pass