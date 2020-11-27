# cordcloud 自动续命
import requests, pickle
import json
import os

# 需要使用代理才能够访问,先使用系统的代理,希望可以改成直接使用shadowsocks
proxies = {
  "http": "http://127.0.0.1:7890",
  "https": "http://127.0.0.1:7890"
}

username = ""
password = ""

cookieFilePath = "cordcloud_cookies"

def login():
    payload = {'email':username,'passwd':password}
    r = requests.post("https://www.cordcloud.site/auth/login",data=payload,proxies=proxies)
    return r.cookies

def check_in(cookies):    
    r = requests.post('https://www.cordcloud.site/user/checkin',cookies=cookies,proxies=proxies)
    content = r.content.decode('unicode-escape')
    try:
        d = json.loads(content)
        print(d['msg'])
        return True
    except:
        # cookie失效的话重新获取cookie
        print('续命失败,可能cookie失效重新获取cookie')
        os.remove(cookieFilePath)
        return False

def check_in_version_2():
    if (os.path.exists(cookieFilePath) == False): 
        cookies = login()
        with open(cookieFilePath, 'wb') as f:
            print('获取cookies成功')
            pickle.dump(cookies, f)
            f.close()
    
    with open(cookieFilePath, 'rb') as f:
        cookies = pickle.load(f)
        f.close()
        return check_in(cookies)

def main():
    i = 1
    while( i <= 3):
        if(check_in_version_2() == True):
            return
        i = i + 1

main()
