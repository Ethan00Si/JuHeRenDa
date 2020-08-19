from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix
import numpy as np

# 按照顺序：信息、财经、新闻、商学院
def read_corpus():
    file_path_list = ['data/语料/cut_words_result/info.txt',
                      'data/语料/cut_words_result/fiance.txt',
                      'data/语料/cut_words_result/news.txt',
                      'data/语料/cut_words_result/business.txt']
    corpus = list()
    for item in file_path_list:
        with open(item, 'r') as fin:
            tmp = [x.strip()[2:] for x in fin.readlines()]
            corpus.append(tmp)
    return corpus

def cal_IDF(X,vocabulary):
    IDF = np.ndarray((len(vocabulary),1))
    for i in range(len(vocabulary)):
        for line in range(X.shape[0]):
            pass


def normalize_TF(tfidf,X,spare=True):
    # 正则化TF
    if spare:
        tmp = X.toarray()
    else:
        tmp = X.copy()
    rows,lines = tmp.shape
    print(rows,lines)
    for i in range(rows):
        max_frequency = max(tmp[i,:])
        if(max_frequency == 0):
            continue
        tfidf[i,:] = tfidf[i,:] / max_frequency
    return tfidf 


# 过滤出关键词，其余删掉
def filt_important_words(vocabulary,tfidf,top_n = 50):
    tmp = tfidf.toarray()
    rows,lines = tmp.shape
    new_vocabulary = dict()
    for i in range(rows):
        tmp_row = np.argsort(-tmp[i,:])
        for j in tmp_row[:top_n]:
            if new_vocabulary.__contains__(j) == False:
                new_vocabulary[j] = vocabulary[j]
    new_tfidf = np.ndarray((tfidf.shape[0],len(new_vocabulary)))
    for i,item in enumerate(new_vocabulary.keys()):
        new_tfidf[:,i] = tmp[:,item]
    ret_vocabulary = dict()
    for i,item in enumerate(new_vocabulary.keys()):
        ret_vocabulary[new_vocabulary[item]] = i
    return ret_vocabulary, new_tfidf


def normalize_tfidf(tfidf):
    rows,lines = tfidf.shape
    for i in range(rows):
        if np.linalg.norm(tfidf[i,:]) == 0: #分母等于0，说明分子也等于0，那就不用处理
            continue
        tfidf[i:i+1,:] = tfidf[i:i+1,:] / np.linalg.norm(tfidf[i,:])
    return tfidf

# 计算矩阵tf-idf
def cal_tf_idf(corpus):

    vectorizer = CountVectorizer()
    # 词汇出现次数和新闻的矩阵
    X = vectorizer.fit_transform(corpus)
    
    # 词汇表
    vocabulary = vectorizer.get_feature_names()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)  

    # 正则化TF TF(t,d)=f/max f_d
    tfidf = normalize_TF(tfidf,X)
    
    # 根据tf-idf的值，挑选出关键词
    vocabulary,tfidf = filt_important_words(vocabulary,tfidf)
    
    tfidf = normalize_tfidf(tfidf)
    
    '''
                doc
      vocabulary|-----------|
                |           |
    metric:     |           |
                |           |
                |-----------|  
    '''
    return tfidf.transpose(),vocabulary

#   创建一个新闻和关键词都tf-idf矩阵
def gen_matrix():
    corpus = read_corpus()
    tmp_cor = corpus[0][0:500]
    for i in range(500):
        tmp_cor.append(corpus[1][i])
    
    tfidf,vocabulary = cal_tf_idf(tmp_cor)
    
    return csr_matrix(tfidf),vocabulary

#  抽取出新的新闻中的vocabulary中有的关键词，产生出现次数的矩阵numpy形式
def extract_feature(news,vocabulary):
    new_matrix = np.ndarray((len(news),len(vocabulary)))
    for i, each_news in enumerate(news):
        # 单独处理一个新闻
        word_occur_times = dict()  #统计新闻中每一个字符出现的次数
        line = each_news.strip().split()
        for word in line:
            if not word_occur_times.__contains__(word):
                word_occur_times[word] = 0
            word_occur_times[word] += 1
        for item in word_occur_times:
            if vocabulary.__contains__(item):
                new_matrix[i, vocabulary[item]] = word_occur_times[item]
                
    return new_matrix.transpose()    
    

           
#   在已经有都矩阵都基础上添加新闻
#   这里的news默认是list存储的新闻切词后的结果
def update_matrix(vocabulary, tfidf, news):
    # 得到 出现次数 矩阵
    new_matrix = extract_feature(news,vocabulary)
    # 生成初始tf-idf
    transformer = TfidfTransformer()
    new_tfidf = transformer.fit_transform(new_matrix)
    # 正则化TF
    new_tfidf = normalize_TF(new_tfidf.toarray(),new_matrix,spare=False)
    # 正则化IDF
    new_tfidf = normalize_tfidf(new_tfidf)
    print(tfidf.shape)
    print(new_tfidf.shape)
    new_matrix = np.concatenate((tfidf.toarray(),new_tfidf), axis=1)
    print(new_matrix.shape)
    return csr_matrix(new_matrix)