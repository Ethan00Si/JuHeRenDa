# 各个学院的老师爬虫及数据处理
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

## process.py中定义函数
- process_majors：处理专业，划分为列表
- getMajors：将列表专业中不重复的写入/data/majors/major_department.txt
- getTeacherName：将教师姓名写入/data/majors/names.txt
- getPosition：将教师职称和职务写入/data/majors/positions.txt
- getLabs：将教师实验室写入/data/majors/labs.txt（**暂时只有信息学院，经济学院的调研室写入了majors中**）

## 待处理任务
- 法学院无法登陆，还在研究
- **处理数据的代码复用性不高，尤其是一些单独处理的点（信息学院的专业），以及将绝对路径转为相对路径**

