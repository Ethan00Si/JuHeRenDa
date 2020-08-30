from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import json


def output_result(news, file_name):
    """
    将dict储存为json文件（会保留原本的内容，即追加写）
    """
    tmp_json = dict()
    with open(file_name,'r') as fin:
        try:
            tmp_json = json.load(fin)
            news.update(tmp_json)
        except:
            pass
    with open(file_name, 'w') as fout:
        json.dump(news,fout, ensure_ascii=False)



def read_corpus(file_path = 'data/语料/cut_words_result/result.json'):
    """
    默认从data/语料/cut_words_result/result.json中读取切词结果
    """
    
    words_dict = dict()
    with open(file_path, 'r') as fin:
        words_dict = json.load(fin)
    mapping = dict() # 新闻在数据库article里的id和切词结果的映射关系
    corpus = list()
    for i,item in enumerate(words_dict) :
        mapping[item] = i
        corpus.append(words_dict[item])
    output_result(mapping, 'data/语料/cut_words_result/mapping.json')
    return corpus

# 使用词汇出现次数的矩阵和vocabulary计算出与vocabulary对应的IDF


def cal_IDF(X, vocabulary):
    """
    返回结果是当前vocabulary的 每一列 对应的IDF
    """
    IDF = np.zeros((1, len(vocabulary)))
    total_news = X.shape[0]  # 新闻总数
    for i in range(len(vocabulary)):
        non_zero = np.count_nonzero(X[:, i])
        # log( (1+N)/(1+DF) ) + 1
        # 这里假设有一个包含所有单词的文档，除此之外加一个1保证IDF非0
        IDF[0, i] = np.log10((1+total_news)/(1+non_zero)) + 1
    
    return IDF[0:1]


# 使用词汇出现次数的矩阵 和 单词对应的IDF值，计算出初始的tf-idf
def cal_raw_tf_idf(X, IDF):
    tfidf = np.zeros(X.shape)
    rows = X.shape[0]
    for i in range(rows):
        tfidf[i, :] = X[i, :]*IDF
    return tfidf


def normalize_TF(tfidf, X, sparse=True):
    # 正则化TF
    if sparse:
        tmp = X.toarray()
    else:
        tmp = X.copy()
    rows, lines = tmp.shape
    #print(rows, lines)
    for i in range(rows):
        max_frequency = max(tmp[i, :])
        if(max_frequency == 0):
            continue
        tfidf[i, :] = tfidf[i, :] / max_frequency
    return tfidf


# 过滤出关键词，其余删掉
def filt_important_words(vocabulary, tfidf, top_n=50):
    """
    return vocabulary :   词汇 对应 列号  （eg：'北京市科委': 11190, '海淀区政府': 11191, '联谊会': 11192）
    """
    tmp = tfidf.copy()
    rows, lines = tmp.shape
    new_vocabulary = dict()
    for i in range(rows):
        tmp_row = np.argsort(-tmp[i, :])
        for j in tmp_row[:top_n]:
            if new_vocabulary.__contains__(j) == False:
                new_vocabulary[j] = vocabulary[j]
    new_tfidf = np.zeros((tfidf.shape[0], len(new_vocabulary)))
    for i, item in enumerate(new_vocabulary.keys()):
        new_tfidf[:, i] = tmp[:, item]
    ret_vocabulary = dict()
    for i, item in enumerate(new_vocabulary.keys()):
        ret_vocabulary[new_vocabulary[item]] = i
    return ret_vocabulary, new_tfidf


def normalize_tfidf(tfidf):
    rows, lines = tfidf.shape
    for i in range(rows):
        if np.linalg.norm(tfidf[i, :]) == 0:  # 分母等于0，说明分子也等于0，那就不用处理
            continue
        tfidf[i:i+1, :] = tfidf[i:i+1, :] / np.linalg.norm(tfidf[i, :])
    return tfidf

# 计算矩阵tf-idf


def cal_tf_idf(corpus):

    vectorizer = CountVectorizer()
    # 词汇出现次数和新闻的矩阵
    X = vectorizer.fit_transform(corpus)

    # 词汇表
    vocabulary = vectorizer.get_feature_names()
    IDF = cal_IDF(X.toarray(), vocabulary)

    tfidf = cal_raw_tf_idf(X.toarray(), IDF)
    # 正则化TF TF(t,d)=f/max f_d
    tfidf = normalize_TF(tfidf, X)

    # 根据tf-idf的值，挑选出关键词
    vocabulary, tfidf = filt_important_words(vocabulary, tfidf)

    tfidf = normalize_tfidf(tfidf)

    # 计算并保存IDF
    new_X = extract_feature(corpus, vocabulary)
    IDF = cal_IDF(new_X, vocabulary)
    '''
                vocabulary
             doc|-----------|
                |           |
    metric:     |           |
                |           |
                |-----------|  
    '''
    return tfidf, vocabulary, IDF

#   创建一个新闻和关键词都tf-idf矩阵


def construct_matrix():
    """
    默认：
    1. 从data/语料/cut_words_result/result.json中读取切词结果
    2. vocabualry recommender_system/CB/storage/vocabulary.json
       vocabulary :   词汇 对应 列号  （eg：'北京市科委': 11190, '海淀区政府': 11191, '联谊会': 11192）
    3. tfidf : 
                    vocabulary
             doc|-----------|
                |           |
    metric:     |           |
                |           |
                |-----------|  
        存储在 recommender_system/CB/storage/tfidf.npy
    4. IDF： 返回结果是当前vocabulary的 每一列 对应的IDF
        保存在 recommender_system/CB/storage/IDF.npy
    """
    corpus = read_corpus()
    
    tfidf, vocabulary, IDF = cal_tf_idf(corpus)
    
    output_result(vocabulary, 'recommender_system/CB/storage/vocabulary.json')
    np.save("recommender_system/CB/storage/tfidf.npy", tfidf)
    np.save("recommender_system/CB/storage/IDF.npy", IDF)
    #return tfidf, vocabulary, IDF


#  抽取出新的新闻中的vocabulary中有的关键词，产生出现次数的矩阵numpy形式
def extract_feature(news, vocabulary):
    new_matrix = np.zeros((len(news), len(vocabulary)))
    for i, each_news in enumerate(news):
        # 单独处理一个新闻
        word_occur_times = dict()  # 统计新闻中每一个字符出现的次数
        line = each_news.strip().split()
        for word in line:
            if not word_occur_times.__contains__(word):
                word_occur_times[word] = 0
            word_occur_times[word] += 1
        for item in word_occur_times:
            if vocabulary.__contains__(item):
                new_matrix[i, vocabulary[item]] = word_occur_times[item]
    '''
    行对应新闻
    列对应关键词
    '''
    return new_matrix


#   在已经有都矩阵都基础上添加新闻
#   这里的news默认是list存储的新闻切词后的结果
def add_news_to_matrix(vocabulary, old_tfidf, news, IDF):
    # 得到 出现次数 矩阵
    new_matrix = extract_feature(news, vocabulary)
    tfidf = cal_raw_tf_idf(new_matrix, IDF)
    tfidf = normalize_TF(tfidf, new_matrix, sparse=False)
    tfidf = normalize_tfidf(tfidf)

    new_matrix = np.concatenate((old_tfidf, tfidf), axis=0)
    #print(new_matrix.shape)
    np.save("recommender_system/CB/storage/tfidf.npy", new_matrix)
    #return new_matrix

def update_matrix(new_file_path):
    """
    用新切出来的新闻增加到原本的tf-idf矩阵中
    """
    corpus = read_corpus(file_path=new_file_path)
    old_tfidf = np.load("recommender_system/CB/storage/tfidf.npy")
    IDF = np.load("recommender_system/CB/storage/IDF.npy")

    vocabulary = dict()
    with open("recommender_system/CB/storage/vocabulary.json",'r') as fin:
        vocabulary = json.load(fin)
    
    add_news_to_matrix(vocabulary,old_tfidf,corpus,IDF)

update_matrix("data/语料/cut_words_result/new_result.json")