# 爬虫
## 实现功能
- 直接在teacher目录下运行
    ```
    scrapy crawl teacher
    ```
- 必要时更换ip池，代码中未import ip.py，所以需要手动更新列表
- settings中定义user-agent池和ip池
- middleware中TeacherDownloaderMiddleware用于更换user-agent
- middleware中ProxyMiddleware用于更换ip，同时在使用ip的情况下，如果当前response中ip被ban则更换ip
- **适用于第一个网页是简单资料，且罗列所有信息，每条信息对应详细介绍页，即Index->Detail**

## 爬虫实现思路
- 把每个学院的教师页分为列表页和详细页，在列表页、详细页都传入某些属性的xpath入口，并且每个属性支持使用不同的正则表达式处理
- 如果要爬取别的属性，可以在配置文件中加入其xpath入口以及需要的正则表达方式

## config文件：
- brief_entry：教室列表中各教师的基础信息xpath（列表）
- properties：主页的待提取属性和其xpath、正则模式，一个属性可以对应多个入口
- properties_detail：详细信息页的待提取属性和其xpath、正则模式的**列表**，支持一个属性对应多个入口，将每个入口内容用逗号拼接后存入该属性中，支持直接从一个入口得到对应属性的值的列表(需设置getall=True)
- properties_extra：特别用于使用refer_dict的网站，用于提供除了refer_dict可以使用的范围下能够提取到的属性外其余需要纳入的属性的xpath和正则模式
- refer_dict：有些网站会把结构化的信息以xx：xxxx的形式存储在一个div中，这样只需要提取前者作为key，提取后者作为value即可存入json，refer_dict就是中文名和英文之间的对应方式，在config文件中设为布尔值，代表该网站是否是这样的网站
- further_explore：是否进入教师详细信息页采集信息
- extra_info：是否进行额外信息的采集，仅当refer_dict为真时才需要
- href_entry：教师详细页的xpath
- next_extry：下一页的xpath
- pattern_further：refer_dict的key和value正则匹配模式
- department：学院名称