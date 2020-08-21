import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
import json
import random
import time

def get_agent():
    user_agent_list = ['Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
                       'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
                       'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
                       'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
                       'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']
    index = random.randint(0, len(user_agent_list)-1)
    return user_agent_list[index]


def get_proxy():
    proxies = [
        {"http":'http://59.110.153.189:80'},
        {"http":'http://101.4.136.34:81'}, 
        {"http":'http://118.31.250.72:8080'}
    ]
    index = random.randint(0, len(proxies)-1)
    return proxies[index]


def read_config():
    path = input("type the config file name:\n")
    path = '/Users/sizihua/Desktop/DaChuang/crawlers/news_each_college/crawler/parse_code/parse_config/'+path
    with open(path, 'r') as fin:
        load_dict = json.load(fin)
    return load_dict


def read_urls(name):
    urls = []
    path = '/Users/sizihua/Desktop/DaChuang/crawlers/news_each_college/crawler/raw_data/urls/'+name
    with open(path, 'r+') as fin:
        for i, item in enumerate(fin):
            line = item.strip()
            urls.append(line)
    return urls


def donnot_allow(url, donnot_list):
    for item in donnot_list:
        if url.find(item) != -1:
            return False
    return True


def output_result(news_titles, news_dates, news_contents, news_urls, domain):
    news_sources = []
    for i in range(len(news_contents)):
        news_sources.append(domain)
    news_data = pd.DataFrame(
        {'datetime': news_dates, 'source': news_sources, 'url': news_urls, 'title': news_titles, 'content': news_contents})
    return news_data

# delay的时间在 1～delay 秒 之间，随机产生
def get_request(url,proxy_open=False,delay=0):
    i = 4
    if delay > 0:
        time.sleep(random.randrange(100,delay*100,25)/100)
    #max retry 3
    while(i > 3):
        user_agent = get_agent()
        headers = {'User-Agent': user_agent}
        try:
            if proxy_open == True:
                proxy = get_proxy()
                r = requests.get(url=url, headers=headers, timeout=5, proxies=proxy)
            else:
                r = requests.get(url=url, headers=headers, timeout=5)
            return r
        except:
            i = i - 1
    return None

def parse_using_find(divs,config,pattern,return_tag=False):
    #print(config)
    #print(pattern)
    if config['config'][pattern].__contains__('attrs') == False:
        res = divs.find(name=config['config'][pattern]['name'])
    else:
        res = divs.find(name=config['config'][pattern]['name'],attrs=config['config'][pattern]['attrs'])
    if res is None:
        print('parse using find failed. config incorrect! error type 1\n')
        return 'NULL'
    else:
        if return_tag == True:
            return res
        else:
            return res.text.strip()

def parse_using_find_all(divs,config,pattern):
    
    if config['config'][pattern].__contains__('attrs') == False:
        res = divs.find_all(name=config['config'][pattern]['name'])
    else:
        res = divs.find_all(name=config['config'][pattern]['name'],attrs=config['config'][pattern]['attrs'])
    if len(res) == 0:
        print('parse using find all failed. config incorrect! error type 1\n')
        return 'NULL'
    else:
        ans_str = str()
        for item in res:
            ans_str += item.text.strip()
        return ans_str


def parse_ini(divs,config,pattern):
    if config['config'][pattern].__contains__('further_parse') == False:
        if config['config'][pattern].__contains__('find_all'):
            return parse_using_find_all(divs,config,pattern)
        else:
            return parse_using_find(divs,config,pattern)
    else:
        first = parse_using_find(divs,config,pattern,return_tag=True)
        #print(pattern)
        #print(first)
        if(first == "NULL"):
            return first
        if config['config'][pattern]['further_parse']['config'][pattern].__contains__('find_all'):
            return parse_using_find_all(first,config['config'][pattern]['further_parse'],pattern)
        else:
            return parse_using_find(first,config['config'][pattern]['further_parse'],pattern)

def parse_html(config):
    urls = read_urls(config['url_file'])

    news_titles = []
    news_dates = []
    news_contents = []
    news_urls = []
    news_sources = []
    news_data = pd.DataFrame(
        {'datetime': news_dates, 'source': news_sources, 'url': news_urls, 'title': news_titles, 'content': news_contents})

    for i, url in enumerate(urls):
        if donnot_allow(url, config['donnot_allow']) == False:
            continue
        r = get_request(url, proxy_open=False, delay=5)
        if r is None:
            continue
        #r.encoding = 'utf-8'
        r.encoding = 'gb18030' 
        '''
        只有新闻学院、文学院是这样
        '''
        page = r.text

        soup = BeautifulSoup(page, 'html.parser')
        # 学院所有的新闻在这个下面
        divs = parse_using_find(soup, config, 'out_layer', return_tag=True)
        #print(divs)
        #exit(0)
        divs = soup
        if divs == 'NULL':
            continue
       
        content = parse_ini(divs, config,'content')
        #print(content)
        #exit(0)
        
        if content == 'NULL':
            print('\n ',i,' parse fail. content error!\n')
            continue
        
        
        title = parse_ini(divs, config, 'title')
        print(title)
        if title == 'NULL':
            print('\n ',i,' parse fail. title error!\n')
            continue
        date = parse_ini(divs,config,'date')
        #print(date)
        #exit(0)
        news_titles.append(title)
        news_dates.append(date)
        news_contents.append(content)
        news_urls.append(url)
        print(i)

        if len(news_urls) == 100:
            news_pd = output_result(
                news_titles, news_dates, news_contents, news_urls, config['domain'])
            news_data = news_data.append(news_pd)
            news_data.to_csv('temp_output2.csv')
            news_contents = []
            news_urls = []
            news_dates = []
            news_titles = []

    if len(news_contents) != 0:
        news_pd = output_result(news_titles, news_dates,
                                news_contents, news_urls, config['domain'])
        news_data = news_data.append(news_pd)

    news_data.to_csv(config['output_file_name'])


def main():
    all_config = read_config()
    for item in all_config:
        parse_html(all_config[item])
        

if __name__ == '__main__':
    main()
