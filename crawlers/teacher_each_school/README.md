# 各个学院的老师爬虫
    暂时：商、经济、财金、信息、新闻、法

## 目录结构及功能说明    
    D:.
    ├─crawler                   //scrapy框架
    │  └─teacher
    │      │  config.json           //配置文件（经济、商、信息、财金、新闻学院）
    │      │  config_sf.json        //财金的单独配置文件（捕获专业）
    │      │  config_info_labs.json //信院实验室的单独配置文件
    │      │  config_news.json      //新闻学院的单独配置文件，从config中剥离，用于测试ip池
    │      │  README.md
    │      │  scrapy.cfg
    |      |  ip.py                 //获取ip地址
    │      │
    │      └─teacher
    │          │  items.py          //定义需要捕获的教师属性
    │          │  middlewares.py    //定义切换user-agent和proxy的中间件
    │          │  pipelines.py      //定义输出文件的位置、形式等
    │          │  settings.py       
    │          │  __init__.py
    │          │
    │          ├─spiders
    │          │  │  teacher.py     //爬虫
    │          │  │  __init__.py
    │          │  │
    │          │  └─__pycache__
    │          │          teacher.cpython-37.pyc
    │          │          __init__.cpython-37.pyc
    │          │
    │          └─__pycache__
    │                  items.cpython-37.pyc
    │                  middlewares.cpython-37.pyc
    │                  pipelines.cpython-37.pyc
    │                  settings.cpython-37.pyc
    │                  __init__.cpython-37.pyc
    │
    └─process                   //处理数据
        │  email.ipynb          //处理邮箱（将AT转为@）
        │  major.ipynb          //处理专业（将每个教师的专业方向由字符串转为列表，同时统计每个学院所有不重复的专业，将其写入文件）
        │  labs.ipynb           //处理实验室（其实暂时只有信息学院）
        │  names.ipynb          //处理教师姓名（将所有学员所有老师姓名存入一个txt）
        │  process.py           //处理教师数据的函数定义
        │
        └─__pycache__
                major.cpython-37.pyc

## 实现功能
- 直接在teacher目录下运行
    ```
    scrapy crawl teacher
    ```
- 必要时更换ip池，代码中未import ip.py，所以需要手动更新列表
- settings中定义user-agent池和ip池
- middleware中TeacherDownloaderMiddleware用于更换user-agent
- middleware中ProxyMiddleware用于更换ip，同时在使用ip的情况下，如果当前response中ip被ban则更换ip
- 将教师专业用列表表示
- 将教师邮箱处理
- 将教师职称汇集到字典中

## process.py中定义函数
- process_majors：处理专业，划分为列表
- getMajors：将列表专业中不重复的写入/data/majors/major_department.txt
- getTeacherName：将教师姓名写入/data/majors/names.txt
- getPosition：将教师职称和职务写入/data/majors/positions.txt
- getLabs：将教师实验室写入/data/majors/labs.txt（**暂时只有信息学院，经济学院的调研室写入了majors中**）

## 爬虫实现思路
- 把每个学院的教师页分为列表页和详细页，在列表页、详细页都传入某些属性的xpath入口，并且每个属性支持使用不同的正则表达式处理
- 如果要爬取别的属性，可以在配置文件中加入其xpath入口以及需要的正则表达方式

## config文件：
- brief_entry：教室列表中各教师的基础信息xpath（列表）
- properties：主页的待提取属性和其xpath、正则模式，仅支持一个属性对应一个入口
- properties_detail：详细信息页的待提取属性和其xpath、正则模式的**列表**，支持一个属性对应多个入口，将每个入口内容用逗号拼接后存入该属性中，支持直接从一个入口得到对应属性的值的列表
- properties_extra：特别用于使用refer_dict的网站，用于提供除了refer_dict可以使用的范围下能够提取到的属性外其余需要纳入的属性的xpath和正则模式
- refer_dict：有些网站会把结构化的信息以xx：xxxx的形式存储在一个div中，这样只需要提取前者作为key，提取后者作为value即可存入json，refer_dict就是中文名和英文之间的对应方式，在config文件中设为布尔值，代表该网站是否是这样的网站
- further_explore：是否进入教师详细信息页采集信息
- extra_info：是否进行额外信息的采集，仅当refer_dict为真时才需要
- href_entry：教师详细页的xpath
- next_extry：下一页的xpath
- pattern_further：refer_dict的key和value正则匹配模式
- department：学院名称

## 待处理任务
- 法学院无法登陆，还在研究
- **处理数据的代码复用性不高，尤其是一些单独处理的点（信息学院的专业），以及将绝对路径转为相对路径**

