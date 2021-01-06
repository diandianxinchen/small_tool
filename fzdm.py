import commonUtil
import requests
from bs4 import BeautifulSoup
import os


# 风之动漫
def get_img_url(pageHtml):
    soup = BeautifulSoup(pageHtml, 'lxml')
    scripts = soup.select("script")
    scripts[0].text
    for script in scripts:
        s = script.string
        if s is not None:
            if s.find("mhurl=") != -1 and s.find("mhss=") != -1:
                start = s.find("mhurl=") + len("mhurl=")
                sub = s[start + 1:]
                end = sub.find("\"", 1)
                mh_url = sub[0:end]
                mh_ss = "http://www-mipengine-org.mipcdn.com/i/p3.manhuapan.com/"
                img_url = mh_ss + mh_url
                return img_url


class Fzdm_download:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        commonUtil.change_base_dir()
        commonUtil.change_dir(self.name)

    # 获取最新的章节
    def get_last(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, features='lxml')
        content = soup.find(id='content')
        link = content.find('a')
        return {'name': link.text, 'href': link.get('href')}

    def download(self):
        last = self.get_last()
        name = last.get('name')
        if commonUtil.check_is_update(name):
            commonUtil.change_dir(name)
            href = last.get('href')
            page_url = commonUtil.get_page_url(self.url, href)
            i = 1
            while True:
                r = requests.get(page_url)
                if r.status_code != 200:
                    print("err, status_code = " + str(r.status_code) + ", url = " + page_url)
                    return
                soup = BeautifulSoup(r.content, features='lxml')
                ele = soup.find("a", class_="pure-button-primary", string="下一页")
                img_url = get_img_url(r.content)
                commonUtil.download_img(img_url, str(i))
                if ele is None:
                    break
                i = i + 1
                index = page_url.rfind("/")
                page_url = page_url[0:index+1] + "index_" + str(i) + ".html"


onePiece = Fzdm_download("海贼王", "https://manhua.fzdm.com/2/")
onePiece.download()
