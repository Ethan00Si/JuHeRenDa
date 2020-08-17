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

def normalize_TF(tfidf,X):
    # 正则化TF
    tmp = X.toarray()
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
    return new_vocabulary, csr_matrix(new_tfidf)


def normalize_tfidf(tfidf):
    rows,lines = tfidf.shape
    tfidf = tfidf.toarray()
    '''
    #临时矩阵,转化为numpy
    tmp_matr = tfidf * tfidf  # *乘代表对应位置相乘 A(0,0)*B(0,0)
    sum_cols = tmp_matr.sum(axis = 1)
    print(tfidf.shape)
    for i in range(rows):
        if(math.sqrt(sum_cols[i])) == 0:
            continue
        tfidf[i,:] = tfidf[i,:] / math.sqrt(sum_cols[i])
    return  csr_matrix(tfidf)
    '''
    for i in range(rows):
        if np.linalg.norm(tfidf[i,:]) == 0:
            continue
        tfidf[i:i+1,:] = tfidf[i:i+1,:] / np.linalg.norm(tfidf[i,:])
    return csr_matrix(tfidf)

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
    print(len(vocabulary))
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

def gen_matrix():
    corpus = read_corpus()
    tmp_cor = corpus[0][0:500]
    for i in range(500):
        tmp_cor.append(corpus[1][i])
    
    tfidf,vocabulary = cal_tf_idf(tmp_cor)
    return tfidf