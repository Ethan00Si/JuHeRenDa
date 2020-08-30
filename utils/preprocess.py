import pandas as pd
import re


def delete(file_path, special_charaters):
    """
    删除content中的特殊字符
    按理说标题中是没有什么奇怪的东西的，就只处理了content
    参数说明：
    1. file_name是要处理的内容的相对路径
    2. special_charaters是特殊字符列表，如果你的新闻有特殊字符请加入，默认只包含\n \r 空格 NULL nan
    """
    
    read_pandas = pd.read_csv(file_path)
    tmp_pandas = read_pandas.copy()
    
    for i,item in enumerate(read_pandas['content']):
        tmp = str(item).replace(' ','')
        for word in special_charaters:
            tmp = tmp.replace(word,'')
        print(i,end='\r')
        tmp_pandas['content'][i] = tmp
    
    for i,item in enumerate(read_pandas['title']):
        tmp = str(item).replace(' ','')
        for word in special_charaters:
            tmp = tmp.replace(word,'')
        print(i,end='\r')
        tmp_pandas['title'][i] = tmp
        

    tmp_pandas.to_csv(file_path, index=False)

def modify_time(file_path, data_position, data_format):
    """
    有一些的时间是 “时间：2020-08-23”，有一些可能是“time: 2020/08/23”
    所以需要先把正确的时间提取出来，再将其转换为pandas 的 format
    参数说明：
    1. file_name是要处理的内容的相对路径
    2. data_position是日期在datatime中所处的位置 例如 '2020-08-23' 对应(0,10) 
    3. data_format是日期格式 '2020-08-23'对应"%Y-%m-%d"，'2020/08/23'对应"%Y/%m/%d"
    """
    read_pandas = pd.read_csv(file_path)
    tmp_pandas = read_pandas.copy()
   
    for i,item in enumerate(read_pandas['datetime']):
        tmp = str(item)[data_position[0]:data_position[1]]
        print(i, end='\r')
        tmp_pandas['datetime'][i] = tmp
    
    tmp_pandas['datetime'] = pd.to_datetime(tmp_pandas['datetime'],format=data_format)
    print(tmp_pandas.head())
    #tmp_pandas.to_csv(file_path,index=False)   
    


