import requests
from lxml import html

link = 'http://www.mzitu.com/89089/{}'
selector = html.fromstring(requests.get('http://www.mzitu.com/89089/1').content)
page = selector.xpath('//div[@class="pagenavi"]/a[last()-1]/span/text()')[0]

def downpicture():
    pic=set()
    for i in range(1,int(page)+1):
        url = link.format(i)
        session = requests.session()
        sel = html.fromstring(session.get(url).content)
        title = sel.xpath('//h2[@class="main-title"]/text()')[0]
        picture = sel.xpath('//div[@class="main-image"]/p/a/img/@src')[0]
        image = session.get(picture).content
        pic.add(picture)
        #print(title,picture)
        filename = '{}.jpg'.format(title)
        with open(filename, 'wb') as f:
            f.write(image)
    return pic

if __name__ == '__main__':
    for i,pic in enumerate(downpicture(),1):
        print(i,pic)