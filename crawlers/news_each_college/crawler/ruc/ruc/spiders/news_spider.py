import scrapy
import json
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from urllib.parse import urljoin

def process_relative(cur_url,to_be_parsed):
    if  to_be_parsed.find('ppt') != -1 or to_be_parsed.find('jpeg') != -1 or to_be_parsed.find('mp4') != -1 or to_be_parsed.find('login') != -1 or  to_be_parsed.find('javascript') != -1 or to_be_parsed.find('@ruc.edu.cn') != -1 or to_be_parsed.find('ebook/') != -1 or to_be_parsed.find('.jpg') != -1 or to_be_parsed.find('.pdf') != -1 or to_be_parsed.find('.doc') != -1 or to_be_parsed.find('.png') != -1 or to_be_parsed.find('.xls') != -1 or to_be_parsed.find('.css') != -1 or to_be_parsed.find('.ppt') != -1 or to_be_parsed.find('.zip') != -1 or to_be_parsed.find('.rar') != -1:
        return None
    return urljoin(cur_url, to_be_parsed)


def process_links(links, current_url, allowed_domin):
    # 补全相对路径 删除指出去的路径
    # 只考虑了简单情况
    links_absolute = list()
    for link in links:
        if link[0:4] == "http" or link[0:3] == "www":
            if link.find('academicfaculty') != -1 or link.find('mp4') != -1 or link.find('login') != -1 or  link.find('javascript') != -1 or link.find('@ruc.edu.cn') != -1 or link.find('ebook/') != -1 or link.find('.jpg') != -1 or link.find('.pdf') != -1 or link.find('.doc') != -1 or link.find('.png') != -1 or link.find('.xls') != -1 or link.find('.css') != -1 or link.find('.ppt') != -1 or link.find('.zip') != -1 or link.find('.rar') != -1:
                continue
            if link.find(allowed_domin) != -1:
                links_absolute.append(link)
        else:
            if len(link) < 2:  # 不知道为什么会匹配到空字符串 可能是html写的不好
                continue
            after = process_relative(current_url, link)
            if after != None:
                links_absolute.append(after)
    return links_absolute


def output_info(links, titles=None, content=None):
    print('\n\n\nlinks:\n')
    for link in links:
        print(link)
    print('\n\n\n')


def write_url(urls,fileName):
    filename = '/Users/sizihua/Desktop/DaChuang/crawlers/news_each_college/crawler/raw_data/urls/'+fileName
    with open(filename, 'w+') as fout:
        for url in urls:
            fout.write(url)
            fout.write('\n')
    


class news_spider(scrapy.Spider):
    name = "news_spider"
    custom_settings = {"RETRY_ENABLED":False}
    allowed_domains = list()
    start_urls = list()
    filename = str()
    header = {
        'Connection': 'keep - alive',  # 保持链接状态
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
    }
    visited = set()
    to_be_parsed = list()
    already_added = set()  #因为中文的关系 parse以后的中文变成16进制表示 所以添加这个 原理上和visited一样 就是防止重复访问


    def start_requests(self):
        config_name = input("type config file name:\n")#example rmbs_config.json
        ini_path = '/Users/sizihua/Desktop/DaChuang/crawlers/news_each_college/crawler/start_config/'+config_name
        load_dict = dict()
        with open(ini_path, 'r') as fin:
            load_dict = json.load(fin)
        for item in load_dict:
            self.allowed_domains.append(load_dict[item]['allowed_domin'])
            start_page = load_dict[item]['start_url']
            self.filename = load_dict[item]['file_name']
            yield scrapy.Request(url=start_page, callback=self.parse, headers=self.header, errback=self.myerrback)

    def parse(self, response):
        '''
        if response.url.find(self.allowed_domains[0]) == -1:
            if not len(self.to_be_parsed) == 0:
                next_url = self.to_be_parsed[0]
                self.to_be_parsed.pop(0)
                print('next: ', next_url, '\n')
                yield scrapy.FormRequest(url=next_url, callback=self.parse, dont_filter=True,errback=self.myerrback)
            else:
                print("call write")
                write_url(self.visited, self.filename)
        '''
        print("\033[31m")
        print("current url: \n")
        print(response.url)
        print('\n\n already parsed :', len(self.visited))
        print("\033[0m")

        self.visited.add(response.url)

        try:
            links = response.xpath('//a/@href').extract()
            
        except:

            if not len(self.to_be_parsed) == 0:
                next_url = self.to_be_parsed[0]
                self.to_be_parsed.pop(0)
                print('next: ', next_url, '\n')
                yield scrapy.FormRequest(url=next_url, callback=self.parse, dont_filter=True, errback=self.myerrback)
                return
            else:
                print("call write")
                write_url(self.visited,self.filename)
                return
        #output_info(links)
        
        # 保证是绝对路径，并且不会指向非ruc的网站
        links = process_links(links, response.url, self.allowed_domains[0])

        for link in links:
            if link not in self.already_added and link not in self.visited and not self.to_be_parsed.__contains__(link):
                if link.find(self.allowed_domains[0]) != -1:
                    self.to_be_parsed.append(link)
                    self.already_added.add(link)
        output_info(links)
        
        print('\n\n number of to be parsed :', len(self.to_be_parsed))
        print('\n\n')

        if (len(self.already_added) % 500 == 0):
            print("call write")
            write_url(self.visited, self.filename)

        if not len(self.to_be_parsed) == 0:
            next_url = self.to_be_parsed[0]
            self.to_be_parsed.pop(0)
            print('next: ', next_url, '\n')
            yield scrapy.FormRequest(url=next_url, callback=self.parse, dont_filter=True, errback=self.myerrback)
        else:
            print("call write")
            write_url(self.visited, self.filename)

    def myerrback(self, failure):
        print("call my error back")
        if not len(self.to_be_parsed) == 0:
            next_url = self.to_be_parsed[0]
            self.to_be_parsed.pop(0)
            print('next: ', next_url, '\n')
            yield scrapy.FormRequest(url=next_url, callback=self.parse, dont_filter=True, errback=self.myerrback)
            return
        else:
            print("call write")
            write_url(self.visited, self.filename)
            return
