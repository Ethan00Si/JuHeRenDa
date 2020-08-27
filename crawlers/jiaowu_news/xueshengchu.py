import requests
from bs4 import BeautifulSoup
from lxml import etree
from urllib import parse
import re
import csv


#写入文件
def write_file(new):
    with open("xuesheng.csv","a+") as csvfile: 
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
        #changed
        item['title']=html_ele.xpath('//div[@class="content-title"]/h3/text()')[0].replace(' ','').replace('\n','').replace('\xa0','')
        print(item['title'])
        #change
        content=soup.find('div',{"class":"v_news_content"}).text
        item['content']=content.replace(' ','').replace('\n','').replace('\xa0','')
        #change
        time=html_ele.xpath('//div[@class="content-title"]/i/text()')[0]
        item['datetime']=re.search(r"(\d{4}-\d{1,2}-\d{1,2})",time).group(0)
        #change
        item['source']='学生处'
        print(item['title'])
        write_file(item)
    except: 
        pass

def _parse(nowurl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    response = requests.get(nowurl, headers=headers)
    html_ele = etree.HTML(response.text)
    #change
    links = html_ele.xpath('//div[@class="txt4"]/h3')
    for link in links:
        newsurl=parse.urljoin(nowurl,link.xpath('./a/@href')[0])
        _getinfo(newsurl)
    
    soup = BeautifulSoup(response.text,'html.parser')
    pid = soup.find(class_='p_next p_fun').findAll('a')
    next_url=pid[0].get('href')   
    next_url = parse.urljoin(nowurl,next_url)	
    if next_url != nowurl and next_url!="":    
        _parse(next_url)


if __name__ == '__main__':
    nowurl=['http://xsc.ruc.edu.cn/index/xwzx.htm']
    
    with open("xuesheng.csv","a+") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["datetime","source","url","title","content"])
    
    for url in nowurl:
        _parse(url)