import pandas as pd
import re

#name_list = ['econ_output.xlsx','finance_outptut.xlsx','info_output.xlsx','journal_outptut.xlsx','law_outptut.xlsx','rmbs_outptut.xlsx']


# 删除所有内容的\n 空格
def delete(file_name):
  
    file_path = '/Users/sizihua/Desktop/DaChuang/data/news_each_school/'
    file_path += file_name
    read_pandas = pd.read_csv(file_path)
    tmp_pandas = read_pandas.copy()
    #read_pandas = read_pandas.rename(columns={'链接':'url','发布时间':'datetime','来源':'source','标题':'title','正文':'content'})
    for i,item in enumerate(read_pandas['content']):
        tmp = str(item).replace(' ','')
        tmp = tmp.replace('\n','')
        tmp = tmp.replace('\r','')
        tmp = tmp.replace('NULL','')
        tmp = tmp.replace('nan','')
        print(i)
        tmp_pandas['content'][i] = tmp
        
    tmp_pandas.to_csv(file_path)  

# 修改date time 有一些是 时间：2020-08-12，把“时间：”删掉
def modify(file_name):
    file_path = '/Users/sizihua/Desktop/DaChuang/data/news_each_school/'
    file_path += file_name
    read_pandas = pd.read_csv(file_path)
    tmp_pandas = read_pandas.copy()
    #read_pandas = read_pandas.rename(columns={'链接':'url','发布时间':'datetime','来源':'source','标题':'title','正文':'content'})
    for i,item in enumerate(read_pandas['datetime']):
        tmp = str(item)[3:]
        
        print(i)
        tmp_pandas['datetime'][i] = tmp
        
    tmp_pandas.to_csv(file_path)  

# 调整时间格式 2020-08-16
def adjust_time(file_name):
    file_path = '/Users/sizihua/Desktop/DaChuang/data/news_each_school/'
    file_path += file_name
    read_pandas = pd.read_csv(file_path)
    tmp_pandas = read_pandas.copy()
    tmp_pandas['datetime'] = pd.to_datetime(tmp_pandas['datetime'],format="%Y-%m-%d")
    #tmp_pandas['datetime'] = pd.to_datetime(tmp_pandas['datetime'],format="%Y/%m/%d")
    #tmp_pandas['datetime'] = pd.to_datetime(tmp_pandas['datetime'],format="%d-%m-%Y")
    tmp_pandas = tmp_pandas.sort_values(by='datetime',ascending=False)
    #del index
    print(tmp_pandas.head())
    tmp_pandas.to_csv(file_path)  

adjust_time('philosophe_output.csv')
#delete('philosophe_output.csv')
#modify('philosophe_output.csv')