'''
从标题里提取出会议名称
'''
import pandas as pd
import jiagu
def read_and_store_title():
    titles = list()
    name_list = ['econ_output.xlsx','finance_outptut.xlsx','info_output.xlsx','journal_outptut.xlsx','law_outptut.xlsx','rmbs_outptut.xlsx']
    for item in name_list:
        sheet = pd.read_excel(io=item)
        for i,line in enumerate(sheet['标题']):
            titles.append(str(line))
    return titles
    '''
    with open('titles.txt','w') as fout:
        for line in titles:
            fout.write(line)
            fout.write('\n')
    '''

#read_and_store_title()
def extract():
    titles = read_and_store_title()

text = '陈彦斌教授受邀参加《关于进一步扩大社会领域民间投资的意见》专家评审会'

words = jiagu.seg(text) # 分词
print(words)

pos = jiagu.pos(words) # 词性标注
print(pos)

ner = jiagu.ner(words) # 命名实体识别
print(ner)