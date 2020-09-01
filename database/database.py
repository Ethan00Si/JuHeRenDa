import mysql.connector
import pandas as pd
import pymysql
# 构建四个表格, 一台机器应该只用构建一次


def construct_tables(cursor):
    create_article = 'CREATE TABLE article ( art_id INT UNSIGNED PRIMARY KEY NOT NULL auto_increment, art_source VARCHAR(32), art_url VARCHAR(255), art_title VARCHAR(255) default \'\', art_content MEDIUMTEXT, art_type VARCHAR(32), art_image VARCHAR(255) DEFAULT \'local image\',art_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, art_legal tinyint default 0,entity_id VARCHAR(255) ,entity_idx VARCHAR(255),relation_id VARCHAR(255)) DEFAULT CHARSET=utf8mb4 ;'

    create_tfidf = 'CREATE TABLE tfidf (word_id INT UNSIGNED PRIMARY KEY NOT NULL auto_increment, word VARCHAR(32), word_idf DOUBLE UNSIGNED, word_col INT UNSIGNED UNIQUE)DEFAULT CHARSET=utf8mb4;'

    create_user_log = 'CREATE TABLE user_log (log_id INT UNSIGNED PRIMARY KEY NOT NULL auto_increment, user_id INT UNSIGNED, behavior INT default 0, behavior_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, art_id INT UNSIGNED)DEFAULT CHARSET=utf8mb4;'

    create_user_file = 'CREATE TABLE user_file (user_id INT UNSIGNED PRIMARY KEY NOT NULL auto_increment, user_name VARCHAR(64),user_number VARCHAR(16) UNIQUE, user_gender TINYINT DEFAULT 0, user_tags VARCHAR(255),user_create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, user_last_login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, user_legal TINYINT default 0)DEFAULT CHARSET=utf8mb4; '

    execute(cursor, create_article)
    execute(cursor, create_tfidf)
    execute(cursor, create_user_log)
    execute(cursor, create_user_file)

# 将数据（列表存储）转化为一个连续的字符串，可以作为sql VALUES的输入


def merge_data(data_list):
    ans_str = list()
    for item in data_list:
        tmp = str(item)
        tmp = '\''+tmp+'\''
        ans_str.append(tmp)
    res = str()
    for i in range(len(ans_str)):
        if i == 0:
            res = '('+ans_str[i]+','
        elif i != len(ans_str) - 1:
            res += ans_str[i]+','
        elif i == len(ans_str) - 1:
            res += ans_str[i] + ');'
    return res


# 一个用来与数据库交互的函数
def execute(cursor, command):
    cursor.execute(command)
    try:
        data = cursor.fetchall()
    except:
        print('fetchall error')
        return
    
    if len(data)==0:
        print('no feedback')
        return

    for item in data:
        print(item[0])


# 向article里面插入新闻
def insert_to_article(cursor,db):
    news_list = [('data/news_each_school/info_output.csv', '信息'),
                 ('data/news_each_school/econ_output.csv', '经济'),
                 ('data/公众号/ruc_info.csv','信火相传'),
                 ('data/教务处/jiaowuchu.csv','教务处')]
    for item in news_list:
        file_path, art_type = item
        data_csv = pd.read_csv(file_path)
        print('current_file: ',file_path)
        for index, row in data_csv.iterrows():
            print(index,end='\r')
            source = str(row['source'])
            url = str(row['url'])
            title = str(row['title'])
            content = str(row['content'])
            if content == 'nan':
                content = ''
            time = row['datetime'].replace('-','')+'000000'
            
            values = (source,url,title,content,art_type,time)
            sql = 'INSERT INTO article (art_source, art_url, art_title, art_content, art_type, art_time) VALUES (%s, %s, %s, %s, %s, %s)'
            # try:
            cursor.execute(sql,  values)
            db.commit()
            # except:
            #     print(values)
            #     exit(0)


'''
连接数据库
'''

# db = pymysql.connect(host='localhost',
#                              port=3306,
#                              user='root',      # 数据库IP、用户名和密码
#                              passwd='123456',
#                              charset='utf8',
#                              database='Dachuang' # 数据库的名字 需要先创建才能连接
# 

'''
db = mysql.connector.connect(
         host='183.174.228.33',
         port = 8282,
         user='root',
         passwd='123456',
         database ='ructoutiao',
         charset='utf8'
)
'''
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

cursor.execute("SET NAMES utf8mb4") # 使用utf8mb4 部分汉字以及所有emoji都是这个
cursor.execute("SET CHARACTER SET utf8mb4")
cursor.execute("SET character_set_connection = utf8mb4")




# 第一次使用的时候先创建tables，再去insert
#construct_tables(cursor)
#insert_to_article(cursor,db)
