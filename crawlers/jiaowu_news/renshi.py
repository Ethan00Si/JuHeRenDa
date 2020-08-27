import requests
from bs4 import BeautifulSoup
from lxml import etree
from urllib import parse
import re
import csv


#写入文件
def write_file(new):
    with open("renshi.csv","a+") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow([new['datetime'],new['source'],new['url'],new['title'],new['content']])

def _getinfo(nowurl):
    item={'datetime':0,'source':0,'url':0,'title':0,'content':0}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    res = requests.get(nowurl,headers=headers)
    res.encoding = 'utf-8'
    html_ele = etree.HTML(res.text)
    soup = BeautifulSoup(res.text,'html.parser')
    item['url']=nowurl
    try:
        
        title=html_ele.xpath('/html/body/div[4]/div[2]/div[2]/div[1]/text()')[0].replace('\n','')
        item['title']=re.sub('\s','',title)
        print(item['title'])
        #change
        content=soup.find('div',{"class":"neirong"}).text
        item['content']=content.replace(' ','').replace('\n','').replace('\xa0','')
        #changed
        time=html_ele.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/text()[2]')[0]
        item['datetime']=re.search(r"(\d{4}-\d{1,2}-\d{1,2})",time).group(0)
        #change
        item['source']='人事处'
        
        write_file(item)
    except: 
        pass

def _parse(nowurl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    response = requests.get(nowurl, headers=headers)
    html_ele = etree.HTML(response.text)
    links = html_ele.xpath('//ul[@class="iise"]/li')
    for link in links:
        newsurl=parse.urljoin(nowurl,link.xpath('.//a/@href')[0])
        _getinfo(newsurl)
    next_url = html_ele.xpath('/html/body/div[4]/div[2]/table/tbody/tr/td/form/a[3]/@href')[0]
    next_url = parse.urljoin(nowurl,next_url)	
    if next_url != nowurl:    
        _parse(next_url)


if __name__ == '__main__':
    #通知公告，工作动态，招聘信息，下载专区，规章制度
    nowurl=['http://hr.ruc.edu.cn/tzgg/index.htm','http://hr.ruc.edu.cn/gzdt/index.htm','http://hr.ruc.edu.cn/zpxx/index.htm','http://hr.ruc.edu.cn/xzzq/index.htm','http://hr.ruc.edu.cn/gzzd/index.htm']
    
    with open("renshi.csv","a+") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["datetime","source","url","title","content"])
    
    for url in nowurl:
        _parse(url)