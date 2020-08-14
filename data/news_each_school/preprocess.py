import pandas as pd
import re

#name_list = ['econ_output.xlsx','finance_outptut.xlsx','info_output.xlsx','journal_outptut.xlsx','law_outptut.xlsx','rmbs_outptut.xlsx']
name_list = ['ai_output.csv']
path = 'Users/sizihua/Desktop/DaChuang/data/news_each_school/'


# 删除所有内容的\n 空格
def delete():
    for item in name_list:
        file_path = '/Users/sizihua/Desktop/DaChuang/data/news_each_school/ai_output.csv'
        read_pandas = pd.read_csv(file_path)
        tmp_pandas = read_pandas.copy()
        #read_pandas = read_pandas.rename(columns={'链接':'url','发布时间':'datetime','来源':'source','标题':'title','正文':'content'})
        for i,item in enumerate(read_pandas['content']):
            tmp = str(item).replace(' ','')
            tmp = tmp.replace('\n','')
            tmp = tmp.replace('NULL','')
            tmp = tmp.replace('nan','')
            print(i)
            tmp_pandas['content'][i] = tmp
            
        tmp_pandas.to_csv(file_path)  

# 修改date time
def modify():
    for item in name_list:
        file_path = '/Users/sizihua/Desktop/DaChuang/data/news_each_school/ai_output.csv'
        read_pandas = pd.read_csv(file_path)
        tmp_pandas = read_pandas.copy()
        #read_pandas = read_pandas.rename(columns={'链接':'url','发布时间':'datetime','来源':'source','标题':'title','正文':'content'})
        for i,item in enumerate(read_pandas['datetime']):
            tmp = str(item)[3:]
            
            print(i)
            tmp_pandas['datetime'][i] = tmp
            
        tmp_pandas.to_csv(file_path)  

delete()
modify()