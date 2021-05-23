#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @date: 2021/5/16 20:02
# @name: ip反查域名
# @author：h2o0o4

'''
需要注意的问题：
有时候没有一个IP能反查出域名，可能是因为你的IP被网站ban了，而不是查不出来，试着挂个代理
这个接口有时候会因为你的频繁访问而拒绝服务，但是有时候是可以跑出结果的。
'''
import re
import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

list = []  # 用于存放可以通过IP反查到域名的域名


def searchIP(ip: str):
    ip = re.findall('\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}', ip)[0]
    print("IP:{}".format(ip))
    url = "https://dns.aizhan.com/" + ip + "/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    }
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url=url, headers=headers, verify=False, timeout=5)
        # title = re.findall("charset=utf-8;<span>(.*?)</span>", response.text)[0]
        # print(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        for t in soup.find_all('td'):
            a = t.find_all('a')
            if a:
                for j in range(len(a)):
                    url = a[j].attrs['href']
                    print(ip+"反查出的URL:"+url)
                    list.append(ip+":"+url)
    except:
        print("\033[31m[x] 请求错误 \033[0m")


if __name__ == '__main__':
    with open('urls.txt', 'r', encoding='utf-8') as f:
        for line in f:
            searchIP(line)

# 写入文件
with open("result.txt", "w") as f:
    for i in list:
        if i != '':
            f.write(i + "\n")
