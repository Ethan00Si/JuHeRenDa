import requests
import random
import time
import json
import pandas as pd
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

class WxSpider():
    def __init__(self, config):
        '''初始化函数'''
        self.config = config
        self.session = requests.Session()
        self.article_infos = pd.DataFrame({'datetime': [], 'source': [], 'url': [], 'title':[], 'content': []})
        self.__initialize()

    def __initialize(self):
        '''初始化各类参数'''
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'Cookie': self.config.Cookie
        }
        # 访问的基地址
        self.profile_url = 'https://mp.weixin.qq.com/mp/profile_ext'
        # 访问时携带的参数
        self.params = {
                'action': 'getmsg',
                '__biz': self.config.biz,
                'f': 'json',
                'offset': '0',
                'count': '10',
                'is_ok': '1',
                'scene': '124',
                'uin': '777',
                'key': '777',
                'pass_ticket': self.config.pass_ticket,
                'wxtoken': '',
                'appmsg_token': self.config.appmsg_token,
                'x5': '0'
        }
        # 文件储存的地址
        self.save_dir = self.config.save_dir
        # 更新请求头
        self.session.headers.update(self.headers)

    def run(self):
        '''运行的主函数'''
        self.__get_all_urls()
        self.__get_all_articles()
        self.__save_article_infos()

    def __get_all_urls(self):
        '''获取该公众号的所有历史文章的url'''
        print('[INFO]: 开始获取目标公众号的所有文章链接...')

        flag = True
        while True:
            # 测试用报数
            print(len(self.article_infos))
            # 访问基地址并以json的形式储存
            res = self.session.get(self.profile_url, params=self.params, verify=False, timeout=5000)
            # print(res.text)
            res_json = res.json()
            # 该字段表示是否还有剩余的文章
            can_msg_continue = res_json.get('can_msg_continue', '')
            # 该字段表示偏移量
            next_offset = res_json.get('next_offset', 10)
            # 文章信息都存储在该字段
            general_msg_list = json.loads(res_json.get('general_msg_list', '{}'))
            # 更新下次访问的参数
            self.params.update({'offset': next_offset})
            try:
                # 依次访问这一批文章信息
                for item in general_msg_list['list']:
                    # 该字段储存了文章信息
                    comm_msg_info = item.get('comm_msg_info', {})
                    if not comm_msg_info:
                        continue
                    # 获取datetime，若有多篇文章一起发布，则datetime相同
                    timestamp = comm_msg_info.get('datetime', '')
                    # if timestamp < 1546272000: # after 2019
                    if timestamp < 1514736000: # after 2018
                        flag = False
                        break
                    datetime = time.strftime("%Y-%m-%d", time.localtime(timestamp))
                    # 获取title和url
                    app_msg_ext_info = item.get('app_msg_ext_info', {})
                    if not app_msg_ext_info:
                        continue
                    title = app_msg_ext_info.get('title', '')
                    content_url = app_msg_ext_info.get('content_url', '')
                    # 将文章信息保存
                    if title and content_url:
                        self.article_infos.loc[len(self.article_infos)] = [datetime, self.config.name, content_url, title, '']
                    # 若有多篇文章一起发布
                    if app_msg_ext_info.get('is_multi', '') == 1:
                        for article in app_msg_ext_info.get('multi_app_msg_item_list', []):
                            title = article.get('title', '')
                            content_url = article.get('content_url', '')
                            if title and content_url:
                                self.article_infos.loc[len(self.article_infos)] = [datetime, self.config.name, content_url, title, '']
            except:
                print(self.params['offset'])
                self.__save_article_infos()
                break
            if can_msg_continue != 1 or flag == False:
                break
            else:
                time.sleep(1+random.random())

        print('[INFO]: 已成功获取目标公众号的所有文章链接, 数量为%s' % len(self.article_infos))

    def __get_all_articles(self):
        '''获取该公众号的所有历史文章的内容'''
        for index, row in self.article_infos.iterrows():
            # 测试用
            print(index)
            # 获取页面内容
            html = self.session.get(row['url'])
            # bs4解析
            soup = BeautifulSoup(html.content.decode('utf8'), "lxml")
            content_div = soup.find('div', attrs={'class': 'rich_media_content'})
            
            try:
                content = content_div.text
                # iframes可能为空
                iframes = content_div.find_all('iframe')
                # 去除iframe里的乱码
                for iframe in iframes:
                    if iframe.text:
                        content = content.replace(iframe.text, '', 1)
                stop_words = ['\n', '\t', '']
                for word in stop_words:
                    content = content.replace(word, '')
                row['content'] = content
            except:
                row['content'] = ''
                print('[INFO]: 第{}篇文章content为空，url为：{}'.format(index, row['url']))
            time.sleep(1+random.random())

    def __save_article_infos(self):
        '''以csv的形式保存文件'''
        self.article_infos.to_csv(self.save_dir, index=False)


if __name__ == "__main__":
    # import ruc_info
    # wx_spider = WxSpider(ruc_info)
    # import ruc_business
    # wx_spider = WxSpider(ruc_business)
    import ruc_caijing
    wx_spider = WxSpider(ruc_caijing)
    # import ruc_news
    # wx_spider = WxSpider(ruc_news)
    # import ruc_law
    # wx_spider = WxSpider(ruc_law)
    # import ruc_info_qingxie
    # wx_spider = WxSpider(ruc_info_qingxie)
    # import ruc_xueshenghui
    # wx_spider = WxSpider(ruc_xueshenghui)
    # import ruc_qingxie
    # wx_spider = WxSpider(ruc_qingxie)
    wx_spider.run()