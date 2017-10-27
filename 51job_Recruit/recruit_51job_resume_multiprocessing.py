import requests, re, pymongo, time
from lxml import html
from multiprocessing import Pool
# from postdata import data

collection = pymongo.MongoClient(host='localhost', port=27017)['Falonie'][
    'Recruit_51Job_Resume_tianjin_multiprocessing']

test_url = 'https://ehire.51job.com/Candidate/ResumeView.aspx?hidUserID=351435784&hidEvents=23&pageCode=3&hidKey=35da588ff3fb0a55dc77c36433c91901'
url4 = 'http://ehire.51job.com/Candidate/ResumeView.aspx?hidUserID=28822690&hidEvents=23&pageCode=3&hidKey=db5c7f04c7a572aa4fb4833f42856d8e'
url = 'https://ehire.51job.com/Candidate/SearchResumeNew.aspx'
header = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
cookie = {
    'Cookie': '51job=cenglish%3D0%26%7C%26; guid=15090891709344000090; EhireGuid=8dc46fbeae6e409090ef9a8faea6e69b; ASP.NET_SessionId=1jtrbivpevxhn0ukmdfh1ej1; AccessKey=e249dcab82a5432; RememberLoginInfo=member_name=E2BF04DB6CCD2D50FAD638DD50DCF144&user_name=E2BF04DB6CCD2D50FAD638DD50DCF144; HRUSERINFO=CtmID=2585839&DBID=3&MType=02&HRUID=2965014&UserAUTHORITY=1100111011&IsCtmLevle=1&UserName=%e8%b6%85%e4%b9%90%e5%81%a5%e5%ba%b7&IsStandard=0&LoginTime=10%2f27%2f2017+15%3a27%3a42&ExpireTime=10%2f27%2f2017+16%3a23%3a54&CtmAuthen=0000011000000001000110010000000011100001&BIsAgreed=true&IsResetPwd=0&CtmLiscense=2&AccessKey=8b7ed741015ef9d2; LangType=Lang=&Flag=1; KWD=SEARCH='}
data = {
    # 'ctrlSerach$hidSearchValue':'#天津|050000#0#物流/仓储|0800###################近6个月|5##1#0###0#0#0',
    # 'ctrlSerach$hidSearchValue':'#天津|050000#0#物流/仓储|0800###################近6个月|5######0#0#0',
    'ctrlSerach$hidSearchValue': '#天津|050000#0#物流/仓储|0800###################近6个月|5##1#0###0#0#0',
    'pagerTopNew$ctl06': '50',
    # '__EVENTTARGET': '{}'.format(line.strip()),
    # '__EVENTTARGET':'ctrlSerach$search_submit',
    # '__EVENTTARGET':'pagerBottomNew$btnNum_mi',
    # '__EVENTTARGET':'pagerBottomNew$btnNum2',
    # '__EVENTTARGET': 'pagerBottomNew$btnNum3',
    # '__EVENTTARGET':'pagerBottomNew$btnNum1',
    '__EVENTTARGET': 'pagerBottomNew$btnNum4',
    # '__EVENTTARGET':'pagerBottomNew$btnNum5',
    # '__EVENTTARGET':'pagerBottomNew$btnNum_ma',
    # '__VIEWSTATE':'/wEPDwUJODA0MTA0NTMxDxYMHgRJc0VOaB4IUGFnZVNpemUCMh4QdnNTZWxlY3RlZEZpZWxkcwUzQUdFLFdPUktZRUFSLFNFWCxBUkVBLFdPUktGVU5DLFRPUERFR1JFRSxMQVNUVVBEQVRFHglQYWdlSW5kZXgCCh4IUGFnZURhdGEFkxE0MDF8NjAwfDIwMHw1MDAwfDcyOTA3NTEzLDM2NzE5NjE4NiwzNjcxNjAzMDUsNjQxMDQ2OTAsODU4MDkyNTUsMzY1MTAzNjQ0LDM2MTYxOTEsMzY1Mzg1NTM5LDM2MTQxODQ1MSwzMzI4MDgwNzYsMzQ2MzU3NTYxLDM2NzE4ODcyOSwzMzM0MzYyNTcsNzk0NjY1MDUsMzE0NDc5MDM1LDM1MzY1NjA4NywyODgyMDYwLDYyNjYzMTUzLDMzODUxMjQ4OSwzNjY4NTc1OTEsMzE4MDgwNjA2LDM1NjAxNDE1OSwzMTg3OTMzODEsMzQ2MzYxMTY5LDk1NjY1NzM3LDM2NjE3NTg1OSwzMTQzNTI3MzMsMzY0NTYxNTQ0LDMxMTE3NDUzMCwzNDU2OTk3MDQsMzM2NjM4MTI5LDMzOTQ5NzAzNSwzNDU2MTA2NzcsMzY1NjcwNDk0LDM2NzE0NTM5OCwzNjYxNTg5MjUsMzYzODQzMjgxLDM2NjQzMDMyMiwzNjcyNTA1MjgsMjgzNDU3ODYsMzU2OTcyODE3LDM2NjkxODUyOSw2NDAwNzc1MSwzMzg5OTcwODQsOTQ3MTU4NTMsMzUzMTk1ODg1LDM2Njg5Njc0NywzNjU1OTg3MTEsMzY3MzgxNzY0LDM2NDI0Nzg0NCwzNjU3NjcyNDksMzMzNjIxNzQwLDM2NzM5OTkzOSwzNjczOTk0MzksMzY1MDE1MDIyLDM1MzM0MzU2NywzNTc5NzIzNzksMzY0NjM5ODAyLDMwNjQxODQ1NywzMzg0MzQ0OTcsMzY2MjUwNTM2LDM2NDYwOTQ1MiwzMjQ2MDkzNTQsMzY3Mzk2NDExLDY2NTg4NzA0LDM2NzIyNDk1MiwzMzg2MzMyMjIsMzU5MzUxODE1LDM2NzM1MTg1NSwzNjY4MjkzMTgsMzQ0MzgyNDAxLDMzNDA3OTA2NCw3OTQ3NjkzMCwzNjI4MDY5NzYsMzU4MDExMjY2LDM2NDg3NzMwOSwzNjE2OTcwMjQsMzY0OTY5ODM1LDM2NzM4NTY2NywzNTQ0NTc3MTgsOTI4NDgzMTMsMzY0MDU0ODgwLDM2NzM2NTg1NiwzNTgzOTA2NzIsMzY3MzgyMTc4LDM2NTM1OTQ2NCwzNjYwMDc0NjMsMzY0NDMyMzY3LDM0NjYzMzgyMywzNjcxNzU1NjUsMjkxOTE5MzQsMzU0NjczMTA2LDMwNDEwNjQzNywzMzk5Njc2NjMsMzY0MDA5MDQ4LDMzNDgwMDY2NSwzNjQwOTc4OTQsMzYyNTM3ODU2LDMwNTE0MjUxNiwzMzU1NTY2OTMsMzYyMTE0NTcyLDM1OTY3MTQ2MiwzNjczNzQ0MjAsMzYyNTMwOTYyLDM2NzM3NDU1NSwzMTc4MzcxNjgsMzYxNTQwMzI3LDM2NzMxOTg5MSwzNjQ4Nzg4MjQsMzY0MTU2MzkyLDM1OTY2NTY1MCwzNjcwMzI5NDMsMzY2OTc0NTg3LDM2NzExNzg2MywzMzgwMTAzMzgsMzE4MDUyMTA5LDM1NzI4ODEwOSwzNjUxMTkzNDEsMzY1ODY1NzU2LDM2NDEzODE5OSwzNjczNjYzMDQsMzY3MjIzMjQwLDMyNzgzNTIxMiwzNjEwMzM1NTcsMzQ3MTc1ODg1LDMzMzI0NzAyMCw3MzYyMjA0MiwzNjczNjMwNTAsMzYyOTA3MTg4LDM2NzAyMTQ0MCwzNjUzMjI5NTcsMzA2MjEwMzI4LDM2NjA1NTYyOSwzNjczMDAxNTQsMzU0NzQ3MzA2LDM2Njc3MzE0OSwzMjU3MTYyNDgsMzY2MzgyMTg0LDM2MzI5NTc5MywzMjkzMzAwNDQsMzY3MzU3NzI3LDM0ODIxOTk0MywzNjczNTcwMDUsMzU0MTQ0NTk0LDM1MjU5NTk2NCwzNTkyNzMzMTIsMzY0MjE4NDI5LDM2NzIxMzk4NCwzMzQ3ODc3NzYsMzY3MzUwMDYzLDMwNTI2NzAyMSwzNjczNDU0OTYsMzY0NDgyOTg4LDMyNTc0MDY1MywzMTAxMTQ2ODIsMzUwODQ1MzcyLDk2MDY2NjI4LDMxNDI3MTE0OCwxNDUzODQ5OCwzNjI5NjU4NzEsMzY3MzMxOTQxLDYzMjU3MzIyLDM0Njg1MzgzNSwzNjU4NjEzMjgsMzM5NzkwNTExLDM2MzYxNzc0NCwzNjA0NDk4Njgs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',
    '__VIEWSTATE': '/wEPDwUJODA0MTA0NTMxDxYMHgRJc0VOaB4IUGFnZVNpemUCMh4QdnNTZWxlY3RlZEZpZWxkcwUzQUdFLFdPUktZRUFSLFNFWCxBUkVBLFdPUktGVU5DLFRPUERFR1JFRSxMQVNUVVBEQVRFHglQYWdlSW5kZXgCLh4IUGFnZURhdGEF/RAyMjAxfDI0MDB8MjAwfDUwMDB8MzI3NzgzODQ2LDMyMTUyNTg4NSwzMjA4NjEzMjgsMzE3OTM4NTcwLDM1NDU0NDEzMyw5MTI1MTkwNiwzNjUwMDE2ODUsMzYxOTYxMDAyLDM2NDk4MjczNSw3MzEzODYwNCwzMjY2NzIyNDcsNTY2ODAxNTksMzM3OTk5OTAyLDM2MDY3NTY4MCwzNjQ1NDQ4MjUsMzMzMjY3ODk1LDUzMzE3MDczLDM2NDU3NzQ5NCwzNjQ2MTE5NDQsMzU2ODU5NDIxLDMzOTQ0NTQzMyw3MDU0NzYxOSwzMDU5OTE2NjIsMzUwNjkyNzc5LDM2MzA4ODM2NiwxNjQ4MTgyMSwzNjQwMjEyMTUsMzY0NDQ4NjkzLDM2NDk0OTE0Myw3NDA1ODA0MCwzNjIzOTI4NDIsMzM4NTgxODAyLDM2MzI2NzIxNCwzNjQwMzk2NzcsMzY0OTMwODUyLDMxNTE1OTkwNCwzNjQ5MjI5NzAsMzY0OTIxODgxLDM2MTM0ODQ5MCwzNjQ4NTEwNDEsNTc1Nzc5OTIsNjUyOTY0NTcsMzU5NjMzNTU2LDg1OTIxNzIxLDY1MzU4NzI4LDMzOTE2MDA2OCw3MzIyMDEwOSwzNTc0MzQyMDksMzM2NzgyOTM3LDM2MzQyODkyOCwzMTQwMTAxNTksMzYyNjkxNTYzLDMyMzE0MDQ4Miw1NTkxNTk2MywzMjg1NjU0ODksMzM1NTIyNjU5LDM1OTg3OTgwMCwzNjQ2NTA4MDMsNjU5NDg3NDUsNzIwODU2NTcsMzY0ODcwMTg0LDM2NDUyMDQ1OCwzNjIwNzY0MzUsNzQ2NzI3NDgsMzYyNjE0NTc1LDcyOTAwMDM1LDMzMzk3MTI2NSw5Mzc1OTczMywyMDE5NTc1OSwzNTc5MDU1MjMsMzYxMjM4NzkxLDM2MzEyMjQ5MiwzNTc4ODczMzQsNjgzMTk2ODcsNzU2NjcxMzIsMzU1Mjk2ODY5LDM1NzI1NTQwMCwzMDQwNjk3MTEsNjY5Nzg4OTcsMzY0ODI3MTkxLDM2NDgyMzUzMiwzNjQ4MjI2ODEsMzUyNjczNzM0LDcwMzA0MjgwLDM1OTYzMTE3NiwzNjQ4MTcxODcsMzU0MzU1OTQ4LDM2NDgxMjAxNCwzMjUzODE2MzUsODQ0NDczNzcsMzYxNjk2MjU1LDMwNTc4NzE3MywzNjQ1ODMwODYsMzU4ODYwODA2LDcwOTQ2NTIwLDM2NDc1NDk1OCw4NDE4NjE5MywzNTQzOTAzODAsMzExNzQyMjk5LDMzNTUwNzgwNywzNjI4NDQ5NTEsMzU3Mzc4NDUzLDM1MTM0ODE5OCwzNDAyNDQyOTMsODgyNDQ2NTAsMzUwNjMwODk1LDMwNTE1MTU5NCwzMzA1MjkxNDEsOTEwNDczMzgsMzYxNDExOTEwLDM2NDczOTEyMywzNDU1MzA4OTUsOTUxMzIwNDAsMzU5OTI3NjM5LDM0MTgwOTE3OSwyODI0OTYzMCw4NTk1MzY2MSw1NDk0OTczNywzNjQ1ODcwOTQsMzY0NTUzNzQyLDMyNTQ0OTk4MSwzMjQ0MzQ3MjMsNzYyNzg4MDMsMzU5MjIxNzE2LDM1ODkyMzM3MSwzNjIxMzI0NzIsMzU1NzU5MDU1LDM2NDY2OTA3OCwzNDEwMjY1ODcsMzY0MDI2NDg0LDM2MjcxNDA4Nyw5NjAwMjYzNSw3NTgxNzk1MSwzNjI0MzcyNDIsNjgwNDUyMjMsMzQ3NTk3NTAyLDMyOTA2NTc5NSw4NzU4NTE0MiwzMzI5NzEwMjYsMzE3NDkzMDI3LDM2NDU4NDg0MiwzNTU0Mjg4MDYsMzU2OTc1NTEwLDM2NDE1Mjg4MCw1MTc2NTM2MCwzNTA4Nzg0NDUsMzY0MzkzNzE4LDM1NTgxMjI5Nyw4MDIyMTEzNCwzNTcwMjE1OTAsMzQ2MTExNzI1LDgxNzA2ODQ4LDgwMTI0MDk2LDM2NDU2MDQzNCwzMTQ4MzYyNzQsMzU4NTYzNTY0LDY3NzAwODkyLDMzMDU3ODI4NiwzNDg2NjI4NDUsMzUwNjM2ODU1LDM2MzA4Mzk3NiwzNTIxOTIwNjMsNzUwODg0NjEsMzYwNzExNTMyLDM2MjExNjY3MiwzNTA5MTIzNTcsNTQ4NDc1NzUsMzY0MzI2OTk1LDM2MDc4NjM4MCwz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',
}

r = requests.post(url=url, data=data, headers=header, cookies=cookie).text
selector = html.fromstring(r)


def urls():
    url_list = []
    for i in selector.xpath('//div[@class="Common_list-table"]/table/tbody/tr[@class="inbox_tr1"]|'
                            '//div[@class="Common_list-table"]/table/tbody/tr[@class="inbox_tr2"]'):
        href = i.xpath('td[@class="Common_list_table-id-text"]/span/a/@href')[0]
        ID = i.xpath('td[@class="Common_list_table-id-text"]/span/a/text()')[0]
        # print(ID, 'http://ehire.51job.com/{}'.format(href))
        url_list.append('http://ehire.51job.com/{}'.format(href))
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
            # company = re.sub(r'[#→star←end]', '', str(company))
            period = ''.join(str(i).strip() for i in i.xpath('td/table/tbody/tr[1]/td[2]/span[2]/text()'))
            period = re.sub(r'[\n ]', '', period)
            try:
                industry = i.xpath('td/table/tbody/tr[2]/td[2]/descendant::text()')[0]
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
            time = i.xpath('td/table/tbody/tr[1]/td[1]/text()')[0]
            company = i.xpath('td/table/tbody/tr[1]/td[2]/span[1]/text()')[0]
            # company = re.sub(r'[#→star←end]', '', str(company))
            period = ''.join(str(i).strip() for i in i.xpath('td/table/tbody/tr[1]/td[2]/span[2]/text()'))
            period = re.sub(r'[\n ]', '', period)
            try:
                industry = i.xpath('td/table/tbody/tr[2]/td[2]/descendant::text()')[0]
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


def mongodb_insert_value(item):
    try:
        collection.insert(item)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # print(urls(),urls().__len__(),type(urls()))
    # print(parse_url(test_url))
    # mongodb_insert_value(parse_url(test_url))
    # collection.drop()
    # with Pool(processes=4) as pool:
    #     print(pool.map(parse_url,urls()))
    t0 = time.time()
    with Pool(processes=4) as pool:
        # for i in urls():
        #     print(i)
        #     print(parse_url(i))
        #     mongodb_insert_value(parse_url(i))
        p = pool.map(parse_url, urls())
        print(p, len(p), type(p))
        collection.insert_many(p)
    # collection.drop()
    # for i,j in enumerate(collection.find({}),1):
    #     print(i,j)
    print(time.time() - t0)
    pass