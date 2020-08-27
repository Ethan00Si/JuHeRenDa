from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
import jsonlines
import pandas
import jieba
import os
import re

def getStopList():
    stop = []
    with open('../../data/语料/stopList.txt','r',encoding='utf-8') as g:
        for line in g:
            stop.append(line.strip())
    return stop

def getCorpus():
    corpus = []
    with open(r'D:\codes\Pt_MarkDown\大创\data\corpus_information.txt','r',encoding='utf-8') as f:
        for line in f:
            corpus.append(re.split(' ',line.strip()))
    return corpus

def getDict():
    dictionary = []
    with open('../../data/语料/dictionary.txt','r',encoding='utf-8') as f:
        for line in f:
            dictionary.append(line.strip())
    return dictionary


#mergeDict()