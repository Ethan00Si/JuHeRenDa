from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import jsonlines
import pandas
import jieba
import os

def mergeDict():
    g = open(r'D:\repositories\DaChuang\embeddings\dictionary.txt','w',encoding='utf-8')
    for dir_path,dir_name,file_list in os.walk(r'D:\repositories\DaChuang\data\词典'):
        for filename in file_list:
            if os.path.splitext(filename)[1]=='.txt':
                with open('/'.join([dir_path,filename]),'r',encoding='utf-8') as f:
                    for line in f:
                        g.write(line)
    g.close()

def getStopList():
    stop = []
    with open('stopList.txt','r',encoding='utf-8') as g:
        for line in g:
            stop.append(line.strip())
    return stop

#mergeDict()