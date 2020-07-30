# 各个学院的老师爬虫

## 目录结构
```
D:.
│  config.json          //信息、商、经济、财金、新闻、法学院的配置
│  scrapy.cfg   
│
└─teacher               //scrapy爬虫
    │  items.py
    │  middlewares.py
    │  pipelines.py     //默认将教师文件以json的格式保存在本目录下
    │  settings.py
    │  __init__.py
    │
    ├─spiders
    │  │  teacher.py
    │  │  __init__.py
    │  │
    │  └─__pycache__
    │          teacher.cpython-37.pyc
    │          __init__.cpython-37.pyc
    │
    └─__pycache__
            items.cpython-37.pyc
            middlewares.cpython-37.pyc
            pipelines.cpython-37.pyc
            settings.cpython-37.pyc
            __init__.cpython-37.pyc
```
## 实现功能
- 直接在teacher目录下运行
    ```
    scrapy crawl teacher
    ```
- 必要时更换ip池，代码中未import ip.py，所以需要手动更新列表

## 实现思路
- 把每个学院的教师页分为列表页和详细页，在列表页、详细页都传入某些属性的xpath入口，并且每个属性支持使用不同的正则表达式处理
- 如果要爬取别的属性，可以在配置文件中加入其xpath入口以及需要的正则表达方式

## 待处理任务
- 法学院无法登陆，还在研究
- 爬下来的数据还可以进一步处理，**去除标点，将AT转为@符号**
