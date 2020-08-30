import jieba
import jieba.posseg
import pandas as pd
import re
import mysql.connector
import json

def jieba_cut(sentence, stopList):
    sentence = str(sentence)
    if len(sentence) == 0:
        return None
    words = jieba.posseg.cut(sentence)
    seg_list = [x for x in words if x.word not in stopList]
    seg_list = [x for x in seg_list if not re.match('[0-9A-Za-z]{1,}', x.word)] #大于8个连续的数字或者字母被认为是非法字符
    res_list = list()
    flags = ['x','an','Ng','n','nr','ns','nt','nz','vn'] 
    # ⬆️是所需要的词性，具体对应关系参考下面的链接
    #https://blog.csdn.net/enter89/article/details/80619805
    temp = list()
    for x in seg_list:
        #print(x.word,x.flag)
        if (flags.__contains__(x.flag)) and (len(x.word)>1):
            temp.append(x.word)
    if len(temp) == 0:
        return None
    temp = ' '.join(temp)
    return temp

def output_result(news, file_name):
    tmp_json = dict()
    with open(file_name,'r') as fin:
        try:
            tmp_json = json.load(fin)
            news.update(tmp_json)
        except:
            pass
    with open(file_name, 'w') as fout:
        json.dump(news,fout, ensure_ascii=False)

def jieba_cut_news(file_path, output_name, cursor, stop):
    

    '''
    下面开始对新闻的title和content进行切词
    '''
    news = dict()
    raw_data = pd.read_csv(file_path)
    for index, row in raw_data.iterrows():
        line = str()
        print("index: ",index,end='\r')
        temp1 = jieba_cut(row['title'],stop)
        if temp1 is not None:
            line += temp1
        line += ' '
        temp2 = jieba_cut(row['content'],stop)
        if temp2 is not None:
            line += temp2
        if len(line) > 1:
            sql = "SELECT art_id FROM article WHERE art_url = %s"
            art_url = str(row['url'])
            na = (art_url, )
            cursor.execute(sql, na)
            myresult = cursor.fetchall()

            res_index, = myresult[0]
            #print(res_index,end='\r')
 
            news[res_index] = line
            
    output_result(news, output_name)  



def cut_words(file_path_list):
    '''
    先连接到database
    '''
    db = mysql.connector.connect(host='localhost',
                                 port=3306,
                                 user='root',      # 数据库IP、用户名和密码
                                 passwd='123456',
                                 charset='utf8',
                                 database='Dachuang'  # 数据库的名字 需要先创建才能连接
                                 )

    # db = mysql.connector.connect(
    #         host='183.174.228.33',
    #         port = 8282,
    #         user='root',
    #         passwd='123456',
    #         database ='ructoutiao',
    #         charset='utf8'
    # 使用 cursor() 方法创建一个游标对象 cursor
    # )
    cursor = db.cursor()


    '''
    初始化结巴
    '''
    stop = [line.strip() for line in open('data/语料/stopList.txt','r').readlines() ]
    
    dictionary = [line.strip() for line in open('data/语料/dictionary.txt').readlines() ]
    for item in dictionary:
        jieba.add_word(item, freq=4, tag='n') # 我这里可以没有词性，但是不能没有词频率
    # 启动2个进程
    # jieba支持多进程，处理逻辑是把一篇文章分2半，一个进程处理一半，最后合起来，所以如果文章不长的话，
    # 进程太多可能反而不如不开多进程
    jieba.enable_parallel(2)

    for file_path in file_path_list:
        jieba_cut_news(file_path, 'data/语料/cut_words_result/result.json', cursor, stop)
        