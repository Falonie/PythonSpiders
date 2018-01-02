import requests, re, pymongo, time
from lxml import html
from multiprocessing import Pool
# from postdata import data

collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie']['Recruit_51Job_Resume_directors']

test_url = 'https://ehire.51job.com/Candidate/ResumeView.aspx?hidUserID=351435784&hidEvents=23&pageCode=3&hidKey=35da588ff3fb0a55dc77c36433c91901'
url4 = 'http://ehire.51job.com/Candidate/ResumeView.aspx?hidUserID=28822690&hidEvents=23&pageCode=3&hidKey=db5c7f04c7a572aa4fb4833f42856d8e'
url = 'https://ehire.51job.com/Candidate/SearchResumeNew.aspx'
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
cookie = {
    'Cookie': '51job=cenglish%3D0%26%7C%26; guid=15094380488800880010; EhireGuid=96a5be8e83bb470a8e475ef5e6f579e7; ASP.NET_SessionId=1a25fyvwbgk4xyjust2agdvt; AccessKey=f333c1a70504471; RememberLoginInfo=member_name=E2BF04DB6CCD2D50FAD638DD50DCF144&user_name=E2BF04DB6CCD2D50FAD638DD50DCF144; HRUSERINFO=CtmID=2585839&DBID=3&MType=02&HRUID=2965014&UserAUTHORITY=1100111011&IsCtmLevle=1&UserName=%e8%b6%85%e4%b9%90%e5%81%a5%e5%ba%b7&IsStandard=0&LoginTime=10%2f31%2f2017+16%3a22%3a12&ExpireTime=10%2f31%2f2017+17%3a11%3a47&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=2&AccessKey=e83546cdfa9498f0; KWD=SEARCH=%25e7%2589%25a9%25e6%25b5%2581%25e6%2580%25bb%25e7%259b%2591%2b%25e8%25bf%2590%25e8%25be%2593%25e6%2580%25bb%25e7%259b%2591%2b%25e7%2589%25a9%25e6%25b5%2581%25e7%25bb%258f%25e7%2590%2586%2b%25e8%25bf%2590%25e8%25be%2593%25e7%25bb%258f%25e7%2590%2586%2b; LangType=Lang=&Flag=1'}
data = {
    'ctrlSerach$hidSearchValue': '销售总监 or VP or CIO or CEO or CSO or 副总裁 or 副总经理 or 市场总监 or 客户总监 or 运营招商总监 or 全国区域总监 or 营销总监 or 拓展总监#北京|010000#0####################近6个月|5##1#1###0#0#0',
    'pagerTopNew$ctl06': '50',
    # '__EVENTTARGET': '{}'.format(line.strip()),
    # '__EVENTTARGET': 'ctrlSerach$search_submit',
    # '__EVENTTARGET':'pagerBottomNew$btnNum_mi',
    # '__EVENTTARGET':'pagerBottomNew$btnNum2',
    # '__EVENTTARGET': 'pagerBottomNew$btnNum3',
    # '__EVENTTARGET':'pagerBottomNew$btnNum1',
    '__EVENTTARGET': 'pagerBottomNew$btnNum4',
    # '__EVENTTARGET':'pagerBottomNew$btnNum5',
    '__VIEWSTATE': '/wEPDwUJODA0MTA0NTMxDxYOHgRJc0VOaB4QdnNTZWxlY3RlZEZpZWxkcwUzQUdFLFdPUktZRUFSLFNFWCxBUkVBLFdPUktGVU5DLFRPUERFR1JFRSxMQVNUVVBEQVRFHghQYWdlU2l6ZQIyHgxzdHJTZWxlY3RDb2wFM0FHRSxXT1JLWUVBUixTRVgsQVJFQSxXT1JLRlVOQyxUT1BERUdSRUUsTEFTVFVQREFURR4JUGFnZUluZGV4AgMeCFBhZ2VEYXRhBcYRMXwyMDB8MjAwfDUwMDB8MzE0NDEyMTI0LDYzMTU0NTA4LDkzNjQ1NDQ5LDU5Nzg2NzA5LDMyMTk0NDIyOCwzNDQyNTkwMjUsNDg3NjY1OCw3NTc5MzU4LDU5MTk4MDQzLDM2MDk0MTUyMCwzMjE4MDg2LDMxMTQ0NDMxOCwxNDE2Mjk4MCwzNDg2NDE4NzEsNTczNTcxMzcsMzM2NzU1NDQ1LDMzNzg4MjUzMCwzNTk5MTY5NTYsOTE0NTEyMTAsNDIwNjExOSwzMjQ3MjY3MDgsMzY3NTI5MDEwLDM2NzU0NjQxOSw5MTMzMTk5LDMwNDQyMzA0MywyNTQ0MTgzNSwzNjczNTUxMjUsMzY3NTQ0MzQzLDMxNTk2MDc5Miw3ODAxMjE2MSw0OTI2Mzk3NCwzMjM1MTgwMCwzNjY2NjY1MjgsMzUxMjE1NTA3LDc3MjI1NDMsOTQxNTc5MjUsOTQxMTg0NywzNjc1NDI2OTMsOTk1NTA0OCwxMTY5MDU4NSwzNTY5MjY3NjAsMzUwOTY2MDU5LDEyMDI2MDI0LDU3MDU1MTE2LDU3MzU1MjM2LDU1NjQwOTUsMzY3MjQ4OTU5LDUwMjA4MTQsMjg4NjY2MDksNDk0NjM4NSw1OTIxMTQ3NywzNjYwODUyOTMsNjM4MzM3NTAsMTA3MTA2MTEsMzY2NTMwNDg3LDM2NjM5MDMwOSwzMDM4NzkzNjAsMzA3MTM0NjE0LDM2NzU0MzM0MywzNjc0NzI3MjcsNzE4MTE3NDMsMzYzNTIwNDczLDM2NzU0MjgyMywyOTYxMDIzOSwzNTc3MTc5MzMsNDkyNTExMjgsODg3MDk0NDQsMzY3NDI4NjM2LDUwNDA0NTgsNzM4NDAxMzYsNDcyMjIwNywxODI5ODY2MSwyODQxNDI5LDYxMTI2OTcsOTQ0MDcxNzAsNzE2OTQ1MTYsMzEzOTk4Mjk3LDMwOTYyMzE3NCwyODcxOTk0Niw1Mjc2MjkwMyw3NjkyOTA5NCwyODYxNTQxMywzMjA5NzE5NSwxODU4MzUzNyw1OTU4OTg1OSw4MzA4MjY0LDEyNzU5NDI5LDEzODQ4MjQ4LDgzNDA4OTUzLDc2MzExOTkxLDY1NTE0MTE4LDg5MTYyNDE3LDMzODI3MTUzOSwzNjYxMzM4LDM0NzI2ODkwNywzNjc0NDgxMTksMzU4ODExNDE3LDI4NDE1NDEzLDM2NDIwNjc4MSw1MjY5MzkxLDM1MDY5OTYsMzg0NDk0OSw3ODM2MjQ4MywxNTcxNDM0MywyNDI1NDU0LDM2NjkxNzY3MSwyNjc0NTc2MiwzMTY5MzU1NjEsMzY1NjA2NDI5LDgxMDM4MDY2LDM2NDg0OTUwNiwzMTU5MjI0MzAsNzU2NDExOTEsODcyNjA4MTEsMzEwNjcwMDQzLDU0MzA0NTE3LDM2MjY0NDQ0Miw1OTI1NjIwNCw0MzM4NDMwLDM1MjEzNjU0NCwzNDc5Nzc0NzksNjk2MDM0MTgsNzUwMDY0MjYsMzY1NDUzOTMxLDcwMjgxMTkxLDcwMzUwMTEsMjkyODE0NTcsMzI5Nzk0Nzk4LDMxNzQ2OTg3MCwzMjEwNjIyOTAsMzUxNTQyOTkxLDM0MTQ5Nzk1NSwzNjU2NDU2NjksODkyNTYyNzYsMzYzODM3NzMzLDM2MzI5NDM0NSw3NzAyMDc5MiwzNjc1MzM4NzUsMzQ4OTYyMDI3LDM2NDgxNDQ5MCwzMDU4Nzc0MTIsMzIyOTgyNjMyLDI0ODk4OTEsODM0MDI1Nyw2MTg4NjYwNywzNjA4ODY4MzcsNTkwODY3NzEsMTE0NTcwMTQsNjQwMzYxNywzMzkxMTgzNDgsNzY3MzkzOCwyNjgzMDQ3OCw5Mzc1NTUzOSwyNDc3MDM4MywzNTU4MDg4NDgsMzU4OTAxMDg5LDY4MzgwMjEsMzE1MjA1MjUwLDMzMzQ1MzM5OSwzMjc2NjU4MjgsMTY1MzgyMTksNzA0OTEyODgsOTA1MTA4MjksNzI1MDAzNzQsMzUzODg0NTMwLDM0MTQ0NzMwMSwyMDEzMDk5MywzNjY2MTQ0MDgsMzUwNDMzODA4LDkwOTYzMDgsMzY1MjYxNTMxLDMyNDUyMjEyNCwxODE1OTMzOCwxMzY1NjcyLDM2NzIxMTIxOCwzNjA4NzUyNDQsNzUwNDQyNjQsNjc5MzQwNTksMzAxMzM2NjgyLDE0NDI2OTM1LDQ2NzM5NTksMTA3MDA1ODIsMTMyNTU2NzMsOTQwMjMwMTQsMzEwNDA1OTcsMTkwODA4MTQsNjI1NzY3LDM0ODc4MjEyOCw3Mzc5Nzg3MCwzNDAwNTU0MjAsMzk2ODIwMyw3NTQ2ODcyOCwzNjcyODk3MzgsMTQ3MTAyNDIsMzA1NzU0MzEwLDM1MDg1ODA4NCwzNjY3ODc1NzksNTM3NjkzMyw3NjYwMTY0OCwzMTk5MzEyMTl8TUNNd0l6QWpPWHd3TVRBd01EQjhNREF3TUh3d01Id3dNSHd3TURBd2ZESXdNVGN3TkRNd2ZESXdNVGN4TURNeGZEQXdNREF3TURBd2ZEQXdNREF3TURBd2ZEQjhPWHd3ZkRCOE1Id3dmREF3TURCOE1EQXdNSHd3ZkRCOGZId3dmREI4T1h3NWZEbDhPWHc1ZkRsOE1EQXdNREF3ZkRBd01EQjhNREF3TUh3d01EQXdNREI4T1h3NWZERWpNakF3SXhBUXovcksyOWZjdk9BZ2IzSWdWbEFnYjNJZ1EwbFBJRzl5SUVORlR5QnZjaUJEVTA4Z2IzSWd1TEhYM0xMRElHOXlJTGl4MTl5K3JjRHRJRzl5SU1yUXM2SFgzTHpnSUc5eUlML051NmZYM0x6Z0lHOXlJTlRMMDZyVjBNbk0xOXk4NENCdmNpRElxN242eC9qVDh0ZmN2T0FnYjNJZzA2clArdGZjdk9BZ2IzSWd6ZGpWdWRmY3ZPQVEeDFRvdGFsUmVjb3JkcwKIJxYCAgEPZBYYAgIPDxYEHhFJc0NvcnJlbGF0aW9uU29ydAUBMB4ISXNVc2VySUQFATBkZAIFD2QWAmYPEA8WAh4HQ2hlY2tlZGhkZGRkAgYPDxYEHghDc3NDbGFzcwUXU2VhcmNoX3Jlc3VtZV9idXR0b25fb24eBF8hU0ICAmRkAgcPDxYEHwoFJkNvbW1vbl9pY29uIFNlYXJjaF9idG5fbGFiZWxfYXJyb3dfQ29yHwsCAmRkAggPDxYEHwoFGVNlYXJjaF9yZXN1bWVfYnV0dG9uX291dDIfCwICZGQCCQ8PFgQfCgUUU2VhcmNoX2J0bl9sYWJsZV9ub24fCwICZGQCCg8PFgIeBFRleHQFC+WFsTUwMDAr5p2hZGQCCw8PFgQfCgUqQ29tbW9uX2ljb24gU2VhcmNoX3Jlc3VtZV9idXR0b25fZGlzaW1nX29uHwsCAmRkAgwPDxYEHwoFLENvbW1vbl9pY29uIFNlYXJjaF9yZXN1bWVfYnV0dG9uX2Rpc2ltZ19kb3V0HwsCAmRkAg0PDxYIHwBoHgpQUGFnZUluZGV4AgMfAgIyHwYCiCdkFgICAg8QZGQWAQICZAIODw8WCB8AaB8NAgMfAgIyHwYCiCdkFhACAQ8PFgofDAUDIDEgHg9Db21tYW5kQXJndW1lbnQFATEeB1Rvb2xUaXAFATEfCmUfCwICZGQCAg8PFgofDAUDIDIgHw4FATIfDwUBMh8KZR8LAgJkZAIDDw8WCh8MBQMgMyAfDgUBMx8PBQEzHwplHwsCAmRkAgQPDxYKHwwFAyA0IB8OBQE0Hw8FATQfCgUGYWN0aXZlHwsCAmRkAgUPDxYKHwwFAyA1IB8OBQE1Hw8FATUfCmUfCwICZGQCBg8PFgIfDGVkZAIHDw8WAh8MBQMuLi5kZAIIDw8WBh8PBQMxMDAfDAUDMTAwHw4FAzEwMGRkAg8PEGQQFQ0G5bm06b6EDOW3peS9nOW5tOmZkAbmgKfliKsJ5bGF5L2P5ZywBuiBjOiDvQblrabljoYS566A5Y6G5pu05paw5pe26Ze0BuaIt+WPowzmnJ/mnJvmnIjolqoM55uu5YmN5pyI6JaqBuihjOS4mgbkuJPkuJoJ5a2m5qCh5ZCNFQ0DQUdFCFdPUktZRUFSA1NFWARBUkVBCFdPUktGVU5DCVRPUERFR1JFRQpMQVNUVVBEQVRFBUhVS09VDEVYUEVDVFNBTEFSWQ1DVVJSRU5UU0FMQVJZDFdPUktJTkRVU1RSWQhUT1BNQUpPUglUT1BTQ0hPT0wUKwMNZ2dnZ2dnZ2dnZ2dnZ2RkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYQBQ1jaGtIYXNQaWNfYmFrBQljaGtIYXNQaWMFDGNieENvbHVtbnMkMAUMY2J4Q29sdW1ucyQxBQxjYnhDb2x1bW5zJDIFDGNieENvbHVtbnMkMwUMY2J4Q29sdW1ucyQ0BQxjYnhDb2x1bW5zJDUFDGNieENvbHVtbnMkNgUMY2J4Q29sdW1ucyQ3BQxjYnhDb2x1bW5zJDgFDGNieENvbHVtbnMkOQUNY2J4Q29sdW1ucyQxMAUNY2J4Q29sdW1ucyQxMQUNY2J4Q29sdW1ucyQxMgUNY2J4Q29sdW1ucyQxMg==',
}

r = requests.post(url=url, data=data, headers=header, cookies=cookie).text
selector = html.fromstring(r)


def urls():
    # url_list = []
    # for i in selector.xpath('//div[@class="Common_list-table"]/table/tbody/tr[@class="inbox_tr1"]|'
    #                         '//div[@class="Common_list-table"]/table/tbody/tr[@class="inbox_tr2"]'):
    #     href = i.xpath('td[@class="Common_list_table-id-text"]/span/a/@href')[0]
    #     ID = i.xpath('td[@class="Common_list_table-id-text"]/span/a/text()')[0]
    #     # print(ID, 'http://ehire.51job.com/{}'.format(href))
    #     url_list.append('http://ehire.51job.com/{}'.format(href))
    path = selector.xpath(
        '//div[@class="Common_list-table"]/table/tbody/tr[@class="inbox_tr1"]/td[@class="Common_list_table-id-text"]/span/a/@href|'
        '//div[@class="Common_list-table"]/table/tbody/tr[@class="inbox_tr2"]/td[@class="Common_list_table-id-text"]/span/a/@href')
    url_list = ['http://ehire.51job.com/{}'.format(href) for href in path]
    return url_list


def parse_url(url):
    response = requests.get(url=url, headers=header, cookies=cookie).text
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
            ID = re.findall('<title>\s*(.*?)\s*</title>', response)[0]
            # print(a, company, period, industry, description)
            return {'ID': ID, 'update_time': update_time, 'time': time, 'company': company, 'period': period,
                    'industry': industry, 'scale': scale, 'nature': nature, 'position': position,
                    'description': description}


def main():
    t0 = time.time()
    with Pool() as pool:
        p = pool.map(parse_url, urls())
        # print(p, len(p), type(p))
        print(len(p), type(p))
        for i, j in enumerate(p, 1):
            print(i, j, type(j))
            try:
                collection.insert_one(j)
            except Exception as e:
                print(e)
        # collection.insert_many(p)
    print(time.time() - t0)


if __name__ == '__main__':
    main()
    pass