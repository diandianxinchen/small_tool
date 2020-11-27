import commonUtil
import requests
from bs4 import BeautifulSoup
import os

# 风之动漫 
class Fzdm_download():
    def __init__(self, name, url):
        self.name = name
        self.url = url
        commonUtil.changeDir(self.name)

    # 检查是否有更新
    def check_is_update(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text,features="lxml")
        content = soup.find(id="content")
        a = content.find('a')
        if (os.path.exists(a.text)):
            print("没有更新，最新的为：" + a.text)
            return False
        self.page_url = self.url + a.get("href")
        print("更新,最新话为:" + a.text)
        commonUtil.changeDir(a.text)
        return True
    
    def download(self):
        if (self.check_is_update() == True):
            page_url = self.page_url
            i = 1
            while(True):
                r = requests.get(page_url)
                if (r.status_code != 200):
                    print("err, status_code = " + str(r.status_code) + ", url = " + self.page_url)
                    return
                soup = BeautifulSoup(r.content, features='lxml')
                ele = soup.find("a", class_="pure-button-primary", string="下一页")
                img_url = self.get_img_url(r.content)
                f = open(str(i) + ".jpg","wb")
                r = requests.get(img_url)
                f.write(r.content)
                f.close()
                if (ele == None):
                    break
                i = i + 1
                page_url = self.page_url + "index_" + str(i) + ".html"
    
    
    def get_img_url(self,pageHtml):
        soup = BeautifulSoup(pageHtml, 'lxml')
        scripts = soup.select("script")
        scripts[0].text
        for script in scripts:
            s = script.string
            if (s != None):
                if (s.find("mhurl=") != -1 and s.find("mhss=") != -1):
                    start = s.find("mhurl=") + len("mhurl=")
                    sub = s[start+1:]
                    end = sub.find("\"",1)
                    mhurl = sub[0:end]
                    mhss = "http://www-mipengine-org.mipcdn.com/i/p3.manhuapan.com/"
                    imgUrl = mhss + mhurl
                    return imgUrl

onePiece = Fzdm_download("海贼王","https://manhua.fzdm.com/2/")
onePiece.download()