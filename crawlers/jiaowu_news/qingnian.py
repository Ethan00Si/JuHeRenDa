import requests
from bs4 import BeautifulSoup
from lxml import etree
from urllib import parse
import re
import csv


#写入文件
def write_file(new):
    with open("qingnian.csv","a+") as csvfile: 
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
        item['title']=html_ele.xpath('/html/body/div[5]/div/div/div[2]/div/div[1]/h4/text()')[0].replace(' ','').replace('\n','').replace('\xa0','')
        #change
        content=soup.find('div',{"class":"txt"}).text
        item['content']=content.replace(' ','').replace('\n','').replace('\xa0','')
        #change
        time=html_ele.xpath('/html/body/div[5]/div/div/div[2]/div/div[1]/span/text()')[0]
        item['datetime']=re.search(r"(\d{4}-\d{1,2}-\d{1,2})",time).group(0)
        #change
        item['source']='青年网'
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
    links = html_ele.xpath('//ul[@class="pic_list"]/li')
    if links==[]:
        links = html_ele.xpath('//ul[@class="normal_list"]/li')
    for link in links:
        newsurl=parse.urljoin(nowurl,link.xpath('.//a/@href')[0])
        _getinfo(newsurl)
    
    soup = BeautifulSoup(response.text,'html.parser')
    pid = soup.find(class_='page_nav').findAll('a')
    next_url=pid[2].get('href')   
    next_url = parse.urljoin(nowurl,next_url)	
    if next_url != nowurl:    
        _parse(next_url)


if __name__ == '__main__':
    #新闻速递，公告栏
    nowurl=['http://youth.ruc.edu.cn/xwsd/index.htm','http://youth.ruc.edu.cn/ggl/index.htm']
    
    with open("qingnian.csv","a+") as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow(["datetime","source","url","title","content"])
    
    for url in nowurl:
        _parse(url)