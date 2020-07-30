# 各个学院的新闻爬虫

## 目录结构

```
.
├── README.md
├── crawler  			//爬虫的代码
│   ├── parse_code			//解析网页 用beautifulsoup
│   │   ├── ip.py					//从免费网站获取可用的ip地址
│   │   ├── parse_config	//解析网页的配置文件
│   │   │   ├── econ.json
│   │   │   ├── finance.json
│   │   │   ├── info.json
│   │   │   ├── journal.json
│   │   │   ├── law.json
│   │   │   └── rmbs.json
│   │   └── parse_with_beautiful.py
│   ├── raw_data			//初始数据
│   │   ├── news
│   │   │   ├── econ_output.xlsx
│   │   │   ├── finance_outptut.xlsx
│   │   │   ├── info_output.xlsx
│   │   │   ├── journal_outptut.xlsx
│   │   │   ├── law_outptut.xlsx
│   │   │   └── rmbs_outptut.xlsx
│   │   └── urls			//所有新闻的链接
│   │       ├── econ_urls.txt
│   │       ├── finance_urls.txt
│   │       ├── info_url.txt
│   │       ├── jcr_urls.txt
│   │       ├── law_urls.txt
│   │       ├── rmbs(all)_urls.txt
│   │       └── rmbs_urls.txt
│   ├── ruc					//scrapy框架的爬虫 用BFS爬取网站所有URL
│   │   ├── ruc
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-37.pyc
│   │   │   │   ├── middlewares.cpython-37.pyc
│   │   │   │   └── settings.cpython-37.pyc
│   │   │   ├── items.py
│   │   │   ├── middlewares.py
│   │   │   ├── pipelines.py
│   │   │   ├── settings.py
│   │   │   └── spiders
│   │   │       ├── __init__.py
│   │   │       ├── __pycache__
│   │   │       │   ├── Ruc_spider.cpython-37.pyc
│   │   │       │   ├── __init__.cpython-37.pyc
│   │   │       │   └── news_spider.cpython-37.pyc
│   │   │       └── news_spider.py
│   │   └── scrapy.cfg
│   └── start_config		#scrapy初始化的配置文件
│       ├── econ_config.json
│       ├── finance_config.json
│       ├── info_config.json
│       ├── journal_config.json
│       ├── law_config.json
│       └── rmbs_config.json
└── news_data				//爬取下来的新闻数据
    ├── econ_output.xlsx
    ├── finance_outptut.xlsx
    ├── info_output.xlsx
    ├── journal_outptut.xlsx
    ├── law_outptut.xlsx
    └── rmbs_outptut.xlsx
```



## 功能介绍

* 先使用scrapy的框架爬取各个网站的所有URL
  * 爬取时候有初步的规则过滤掉不需要的url
  * 使用BFS的方式爬取
* 用beautifulsoup解析已经获取的URL
  * 所有的网站都是一个代码，每个网站都具有自己的配置文件



## 已获取数据

* 已经爬取：信息、财经、经济、法学、新闻、商学院

* 所得到的数据用excel的格式存储，数据还需要处理
  * 有一些数据的时间部分（date）还混有一些别的文字（来源、浏览量等）
  * 大部分数据等内容部分包含大量空格和换行符号，待处理