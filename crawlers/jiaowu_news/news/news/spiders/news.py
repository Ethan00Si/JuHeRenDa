from scrapy import Request
from scrapy.spiders import Spider
from news.items import NewsItem
from urllib import parse
import pandas as pd
import re



class ruc_news(Spider):
    name = 'news'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
    }
			
    def start_requests(self):
        urls=['http://jiaowu.ruc.edu.cn/tzgg6/index.htm',  #教学动态
        'http://jiaowu.ruc.edu.cn/gjjl/index.htm',         #境外交流
        'http://jiaowu.ruc.edu.cn/hdkb2/index.htm',        #活动看板
		'http://jiaowu.ruc.edu.cn/jxdt6/index.htm']        #教学动态
		
        for url in urls:
           yield Request(url=url,headers=self.headers,callback=self.parse) 
        
    
    def parse(self, response):
        links = response.xpath('//ul[@class="iise"]/li')
        nowurl = response.request.url
        newsurls=[]
        for link in links:            
            newsurl=parse.urljoin(nowurl,link.xpath('.//a/@href').extract()[0])
            newsurls.append(newsurl)
			
        for newsurl in newsurls:
            yield Request(url=newsurl, callback=self.new_parse)
			
        next_url = response.xpath('/html/body/div[4]/div[2]/table/tbody/tr/td/form/a[3]/@href').extract()		
        if next_url:
            next_url = parse.urljoin(nowurl,next_url[0])
            yield Request(next_url, headers=self.headers)
	
	
    def new_parse(self, response):
        item = NewsItem()
        sites = response.xpath('//div[@class="dddeii"]/p/span')
        content=[]
        for site in sites:
            s=''.join(site.xpath('text()').extract())
            s=s.replace(' ','')
            s=s.replace('\n','')
            s=s.replace('\xa0','')
            content.append(s)
		
		
        item['content']=''.join(content)
        item['title']=response.xpath('/html/body/div[4]/div[2]/div[2]/div[1]/text()').extract()[0]
        item['url']=response.request.url
        time=response.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/text()').extract()[0]
        item['datetime']=re.search(r"(\d{4}-\d{1,2}-\d{1,2})",time).group(0)
        item['source']='教务处'
		
        yield item
