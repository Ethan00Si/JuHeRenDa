'''
把爬下来的数据进行处理
* 将日期转换为dataframe的时间，并且以此对新闻排序
* 删除内容中的许多空格
'''

import pandas as pd
import re

name_list = ['econ_output.xlsx','finance_outptut.xlsx','info_output.xlsx','journal_outptut.xlsx','law_outptut.xlsx','rmbs_outptut.xlsx']

output_path = '/Users/sizihua/Desktop/DaChuang/data/news_each_school/'
for item in name_list:
    sheet = pd.read_excel(io=item)
    #time_series = list()
    for i,line in enumerate(sheet['发布时间']) :
        line = str(line)
        time = re.search(r"(\d{4}-\d{1,2}-\d{1,2})",line)
        #print(time.group(0))
        if time is None:
            time = re.search(r"(\d{4}/\d{1,2}/\d{1,2})",line)
            if time is not None:
                tmp_line = time.group(0)
            else:
                tmp_line = str()
        else:
            tmp_line = time.group(0)
        sheet['发布时间'][i] = tmp_line
        
    for i,line in enumerate(sheet['正文']):
        line = str(line)
        line = line.strip().replace(' ','')
        sheet['正文'][i] = line

    sheet['发布时间'] = pd.to_datetime(sheet['发布时间'],format="%Y-%m-%d",errors='coerce')
    sheet.index = sheet['发布时间']
    del sheet['发布时间']
    sheet = sheet.sort_index(ascending=False)
    sheet = sheet.drop(columns=['Unnamed: 0'])
    #print(sheet.head())
    file_name = output_path+item
    sheet.to_excel(file_name)
    