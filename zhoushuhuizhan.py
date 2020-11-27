# 检查咒术回战是否有更新
# 地址 https://www.cocomanhua.com/15324/

import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse
from selenium import webdriver

page_url = ''
base_url = ''

def get_url(base_url, path):
    res = urlparse(base_url)
    netloc = res.netloc
    return 'http://' + netloc + path

def changeDir(name):
    if (os.path.exists(name) == False):
        os.mkdir(name)
    os.chdir(name)

def check_is_update(url):
    global page_url
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'lxml')
    ele = soup.find(class_="all_data_list")
    links = ele.find_all("a")
    link = links[0]
    name = link.text
    href = link.get('href')
    if (os.path.exists(name)):
        print("没有更新,最近话为:" + name)
        return False
    os.mkdir(name)
    os.chdir(name)
    page_url = get_url(base_url,href)
    print("有更新，最新话为：" + name + ", " + page_url)
    return True

def download_img(href):
    # 这个网站的处理，没有分析出图片的地址是怎么保存的,用selenium处理
    driver = webdriver.Firefox()
    driver.get(href)
    url = driver.find_element_by_css_selector('.mh_comicpic>img').get_attribute('src')
    driver.close()
    page = 1
    print("链接为:" + url)
    if (url.endswith('.jpg') == False):
        print("无效的链接," + url)
        return
    preUrl = url[0:url.rindex('/') + 1]
    while(True):
        r = requests.get(url)
        if (r.status_code != 200):
            print(str(r.status_code) + ", url = " + url)
            break
        f = open(str(page) + ".jpg", "wb")
        f.write(r.content)
        f.close
        page = page + 1
        url = preUrl + ("%04d" % page) + ".jpg"
    
def Main(name, url):
    global base_url
    base_url = url
    changeDir(name)
    if (check_is_update(url) == True):
        download_img(page_url)    

# download_img('http://www.cocomanhua.com/15324/1/131.html') 
Main('咒术回战','https://www.cocomanhua.com/15324/')
