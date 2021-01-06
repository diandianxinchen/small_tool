import os
from urllib.parse import urljoin
import requests

baseDir = '漫画'
os.path


def change_base_dir():
    if not os.path.exists(baseDir):
        os.mkdir(baseDir)
    os.chdir(baseDir)


def change_dir(name):
    if not os.path.exists(name):
        os.mkdir(name)
    os.chdir(name)


def get_page_url(base_url, href):
    return urljoin(base_url, href)


def download_img(img_url, name):
    if img_url[0] == '"':
        img_url = img_url[1:-1]
    r = requests.get(img_url)
    f = open(str(name) + ".jpg", "wb")
    f.write(r.content)
    f.close()


def check_is_update(name):
    if os.path.exists(name):
        print(name + "没有更新")
        return False
    print(name + "更新了！ 最新话为:" + name)
    return True
