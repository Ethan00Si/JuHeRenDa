import pandas
import re

#将excel转为csv
def transform_to_csv(path):
    excel = pandas.read_excel(path)
    columns = []
    for column in excel.columns:
        if re.search('Unnamed: .*',column):
            columns.append(re.search('Unnamed: .*',column).group())
    print(columns)
    excel.drop(columns=columns,inplace=True)
    
    excel.to_csv(re.search('(.*).xlsx',path).group(1)+'.csv',index=False)

#交换列的顺序,覆盖原csv文件
def exchange_columns(path):
    data = pandas.read_csv(path)
    #data.dropna(axis=0,inplace=True,how='any')
    #data.reset_index(drop=True, inplace=True)

    columns = ['datetime','source','url','title','content']
    data = data.loc[:,columns]
    #for index,content in enumerate(data['content']):
    #    data.loc[index,'content'] = re.sub('\s','',content)
    data.to_csv(path,index=False)

#删除nan和内容中的\r,\n,空格，覆盖原csv文件
def deleteEmpty(path):
    data = pandas.read_csv(path)
    data.dropna(axis=0,inplace=True,how='any')
    data.reset_index(drop=True, inplace=True)
    
    for index,content in enumerate(data['content']):
        data.loc[index,'content'] = re.sub('\s','',content)

    data.to_csv(path,index=False)

#删除重复的行，覆盖原csv文件
def deleteDup(path):
    data = pandas.read_csv(path)
    data.drop_duplicates(inplace=True)
    data.to_csv(path,index=False)
