
# coding: utf-8


import requests
from lxml import etree
import time
import json

valid_proxy_list=[] #记录可用ip地址 例如http：//223.243.5.2：4216

def check_proxy(host,port):
    type = 'http'
    proxies = {}
    proxy_str = "%s://%s:%s" % (type, host, port)
    url = 'http://www.baidu.com/'
    try:
        requests.get(url, proxies={"http":proxy_str})
    except:
        print('connect failed') 
    else:
        valid_proxy_list.append(proxy_str)
        print (proxy_str)
        print ('success')
   

def get_all_proxy():
    url = 'http://cn-proxy.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    html_ele = etree.HTML(response.text)
    links=html_ele.xpath('//*[@id="post-4"]/div/div[4]/table/tbody/tr')
    ip_eles=[]
    port_ele=[]
    for link in links:
        ip_eles.append(link.xpath('.//td[1]/text()'))
        port_ele.append(link.xpath('.//td[2]/text()')) 
    
    for i in range(0,len(ip_eles)):
        check_proxy(ip_eles[i][0],port_ele[i][0])



if __name__ == '__main__':
    get_all_proxy()
    #time.sleep(20)
    print(valid_proxy_list)






