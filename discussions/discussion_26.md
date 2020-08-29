## 架构

爬虫 -> 处理数据，（切词，tf-idf、训练FM，NER，RE） -> 数据库 -> django.model -> django.view（推荐） -> 微信小程序 -> 用户

- 推荐系统：
  - sql数据库
  - 在处理数据层训练fm和tf-idf

- 知识图谱：
  - neo4j
  - 在处理数据层实体识别、关系抽取，识别出的【实体类型、实体值、实体id】存放到新闻数据结构中，#关系存到neo的时候应该带上文章id

- url携带信息：很简单，规定url
- 从外界添加数据：简单，用第三方可 pymysql
- cache保存tf-idf模型和FM模型，**演示**


## 讨论

规定url：现有app如下：
  - 推荐 rucnews/recommender
  - 搜索 rucnews/search
  - 知识库呈现 rucnews/knowledge

规定模板中变量名，可以和数据表中对齐：
  - 新闻：news.title,source,datetime
  - 数据表里是不是按csv中规定的变量名作为Filed的？

**合并数据处理层的各项功能，写成服务，这一层的输入就是raw_data，即爬虫爬下来的东西，输出是将处理后的值分为不同的数据结构添加到数据库中**，我们现在就用信息学院和经济学院，教务处，一个公众号新闻为例做
- 读取的是爬虫爬下来的文件，该训练的训练，该处理的处理
- 存：老师的内容写到图数据库，新闻的内容写到mysql
- 读：用户日志

- process(['~/data/xxx.csv',.....]) // 切词，处理好了数据存到了数据库里
- train() // 读取数据库中相应内容进行训练

1. utils.py
- 切词已有，接口，已实现
- 处理特殊字符，已实现
- 处理特殊时间，统一时间格式，自动填充


## 问题

1. 部署
- python的并行
- 如何让爬虫在后台定时运行
- 三个人的新闻爬虫应该难以整合在一起吧，应该得多个进程（线程？）数据库的写入有没有互斥锁？redis
- nginx
- 发布微信小程序

2. 前后端
- 从前端传回来用户id，文章id，POST/GET 有啥区别？？
- 使用微信自带浏览器打开链接
- **初始化加载tf-idf以及FM模型**
- 邵总铁琦试一下szh的程序能添加成功不
- 有人了解过csrf么？
- 如果用户使用游客登录而不是微人大注册，如何获得其唯一的id？微信

## 任务

一人一个模块，了解自己模块需要的信息，前端、后端、数据库，和之前有了解过相关内容的人对接

szh负责部署基于内容的推荐和个人主页，想办法*爬虫对比时间*，规定新闻数据处理的格式、路径等等

snl负责部署fm，和szh分数加在一起和搜索

- 看django的[教程](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)
- 写view，布置前端
- 接受用户数据，更新用户画像，前后端交互
- *初始化加载推荐要用的模型*
- cache
- 先用现有的数据把前后端互动啥的搞清楚，这两天zpt弄好要新加入文章数据结构中的内容后，再考虑添加多一些，从raw data经过process层之后直接添加进入数据库

zpt负责实体识别
- 设计现有的教师知识库的id表示，将实体加入neo4j
- 学习neo的查找、增添删改方法
- 写弹出窗格的view，布置前端
- （实体对齐）

xyq负责关系抽取，部署项目
- 简单版关系抽取已经实现
- 用户登录的view（选感兴趣的），布置前端，作为游客访问，用微信授权登录
- Nginx部署，*多个爬虫后台运行（scrapy并行？）*
- （复杂版关系抽取）
