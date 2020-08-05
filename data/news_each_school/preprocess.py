import pandas as pd
import re

name_list = ['econ_output.xlsx','finance_outptut.xlsx','info_output.xlsx','journal_outptut.xlsx','law_outptut.xlsx','rmbs_outptut.xlsx']

path='/Users/sizihua/Desktop/DaChuang/data/news_each_school/'

for item in name_list:
    file_path = path+item
    read_pandas = pd.read_excel(file_path)
    read_pandas = read_pandas.rename(columns={'链接':'url','发布时间':'datetime','来源':'source','标题':'title','正文':'content'})
    for i,item in enumerate(read_pandas['content']):
        tmp = str(item).replace(' ','')
        tmp = tmp.replace('\n','')
        read_pandas['content'][i] = tmp
        if tmp == 'nan':
            read_pandas['content'][i] = str()
    read_pandas.to_excel(file_path)  
