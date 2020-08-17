import jieba
import jieba.posseg
import pandas as pd
import re
# 按照顺序：信息、财经、新闻、商学院
# 以下路径使用相对路径，运行程序时处于DaChuang文件夹下即可
# 官网新闻的地址
news_from_web = ['data/news_each_school/info_output.csv',
'data/news_each_school/finance_output.csv',
'data/news_each_school/journal_output.csv',
'data/news_each_school/rmbs_output.csv']

# 公众号新闻的地址
news_from_gzh = ['data/公众号/ruc_info.csv',
'data/公众号/ruc_caijing.csv',
'data/公众号/ruc_news.csv',
'data/公众号/ruc_business.csv'
]

# output file name
output_name_list = ['data/语料/cut_words_result/info.txt',
'data/语料/cut_words_result/fiance.txt',
'data/语料/cut_words_result/news.txt',
'data/语料/cut_words_result/business.txt']


def jieba_cut(sentence, stopList):
    sentence = sentence.replace('\n','')
    sentence = sentence.replace('\r','')
    sentence = sentence.replace(' ','')
    words = jieba.posseg.cut(sentence)
    seg_list = [x for x in words if x.word not in stopList]
    seg_list = [x for x in seg_list if not re.match('[0-9A-Za-z]{1,}',x.word)] #大于8个连续的数字或者字母被认为是非法字符
    res_list = list()
    flags = ['x','an','Ng','n','nr','ns','nt','nz','vn'] 
    # ⬆️是所需要的词性，具体对应关系参考下面的链接
    #https://blog.csdn.net/enter89/article/details/80619805
    temp = list()
    for x in seg_list:
        #print(x.word,x.flag)
        if (flags.__contains__(x.flag)):
            temp.append(x.word)
    if len(temp) == 0:
        return None
    temp = ' '.join(temp)
    return temp

def output_result(news_list,file_name):
    with open(file_name,'w') as fout:
        for line in news_list:
            fout.write(str(line[0]))
            fout.write(' ')
            fout.write(line[1])
            fout.write('\n')


def main():
    ## init jieba
    stop = [line.strip() for line in open('data/语料/stopList.txt','r').readlines() ]
    #jieba.load_userdict('/Users/sizihua/Desktop/DaChuang/data/语料/dic2.txt') 
    dictionary = [line.strip() for line in open('data/语料/dictionary.txt').readlines() ]
    for item in dictionary:
        jieba.add_word(item, freq=4,tag='n') # 我这里可以没有词性，但是不能没有词频率
        
    n_schools = 4 # 目前一共4个学院
    for i in range(n_schools):
        # szh爬取的官网的新闻部分
        news = list()
        raw_data = pd.read_csv(news_from_web[i])
        for index, row in raw_data.iterrows():
            line = str()
            temp1 = jieba_cut(row['title'],stop)
            if temp1 is not None:
                line += temp1
            line += ' '
            temp2 = jieba_cut(row['content'],stop)
            if temp2 is not None:
                line += temp2
            if len(line) > 1:
                news.append( (index,line))
        output_result(news, output_name_list[i])   
        

    
if __name__ == '__main__':
    main()
    