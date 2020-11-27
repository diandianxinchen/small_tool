# xianman123 下载漫画

import commonUtil
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
from urllib.parse import urljoin
import execjs
import json
import re

class download():
    def __init__(self,name,url):
        self.name = name
        self.url = url
        self.url_parse = urlparse(url)
        commonUtil.changeDir(self.name)

    def get_last_update(self):
        r = requests.get(self.url)
        if (r.status_code == 200):
            soup = BeautifulSoup(r.content, features='lxml')
            # 获取最新的一集的名称和链接
            div = soup.find(id='chapterlistload')
            link = div.find("a")
            href = urljoin(self.url, link.get('href'))
            commonUtil.changeDir(link.text)
            return {'name':link.text,'href': href}

    # 是否存在 name
    def check_is_update(self,name):
        return os.path.exists(name) == False
    
    # 通过url 下载该集到本地
    def get_img_url(self, url):
        r = requests.get(url)
        if (r.status_code == 200):
            soup = BeautifulSoup(r.content, features='lxml')
            scripts = soup.find_all("script")
            for script in scripts:
                s = script.string
                # 获取img列表
                if(s != None and s.find('var picdata = ') != -1):
                    index = len('var picdata = ')
                    img_list = json.loads(s[index:-1])
                # 获取img 服务器地址
                if(s != None and s.find('imgDomain') != -1):
                    m = re.search('var imgDomain = (.+)[,;]{1}', s)
                    if m:
                        found = m.group(1)
                        img_domain = found[1:-1]
            res = []
            for item in img_list:
                res.append(urljoin(img_domain, item))
            return res
    
    def download_img(self,name,url):
        r = requests.get(url)
        f = open(name,"wb")
        f.write(r.content)
        f.close()

    def do_download(self):
        res = self.get_last_update()
        if (self.check_is_update(res.get('name'))):
            list = self.get_img_url(res.get('href'))
            i = 1
            for item in list:
                self.download_img(str(i) + ".jpg",item)
                i = i + 1

    
download = download("罗小黑战记·蓝溪镇","https://www.xianman123.com/luoxiaoheizhanjilanxizhen")
download.do_download()