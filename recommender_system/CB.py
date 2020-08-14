from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix
import numpy as np
import math
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

# 正则化 tfidf
'''
def normalize_tfidf(tfidf):
    rows,lines = tfidf.shape
    zeros = 0
    for i in range(rows):
        sum_fenmu = 0.0 # 分母
        for j in range(lines):
            #if tfidf[i,j] == 0:
            #    continue
            sum_fenmu += tfidf[i,j]*tfidf[i,j]
        sum_fenmu = math.sqrt(sum_fenmu)
        if(sum_fenmu == 0):
            zeros += 1
            print(zeros)
            continue
        tfidf[i,:] = tfidf[i,:] / sum_fenmu
    return tfidf
'''

def normalize_tfidf(tfidf):
    rows,lines = tfidf.shape
    tfidf = tfidf.toarray()
    
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
    '''
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
    return tfidf.transpose()

def gen_user_profile(tfidf, user_ratings):
    # 生成用户画像
    user_profile = np.ndarray((tfidf.shape[0], len(user_ratings)))
    # 假设先用5分作为界限，低于5分的没用，高于5分的有用
    for each_user in user_ratings:
        for item in each_user:
            each_user[item] -= 5

    # rocchio algorithm 一般设置 a = 1,b = 0.8, c = 0.1
    b = 0.8
    c = 0.1
    threshold_rate = 1e-10
    tf_idf_matrix = tfidf.toarray()
    for i, each_user in enumerate(user_ratings):
        pos_cnt = 0
        neg_cnt = 0
        '''
        下面这里没有想好相关的新闻和不相关的新闻如何影响user profile，暂定是乘得分作为影响
        '''
        for item in each_user:
            if(each_user[item] > 0):
                pos_cnt += 1
        for item in each_user:
            if(each_user[item] < 0):
                neg_cnt += 1

        for item in each_user:
            if(each_user[item] >= 0):
                user_profile[0:, i:i+1] += b/pos_cnt * tf_idf_matrix[0:, item:item+1]
                #user_profile[0:, i:i+1] += each_user[item]*b/pos_cnt*tfidf[0:, item]
        for item in each_user:
            if(each_user[item] < 0):
                user_profile[0:, i:i+1] -= c/neg_cnt * tf_idf_matrix[0:, item:item+1]
                #user_profile[0:, i:i+1] += each_user[item]*c/neg_cnt*tfidf[0:, item]
    (rows, cols) = user_profile.shape
    
    for i in range(rows):
        for j in range(cols):
            if(user_profile[i, j] < threshold_rate and user_profile[i, j] > -threshold_rate):
                user_profile[i, j] = 0
    
    # np.set_printoptions(threshold=np.inf)
    user_profile = csr_matrix(user_profile)
    # print(user_profile)
    '''
                user
      vocabulary|-----------|
                |           |
    metric:     |           |
                |           |
                |-----------|  
    '''
    return user_profile


def find_top_n_items(scores, index, n=15):
    scores = np.array(scores)
    indecies = np.argsort(-scores)
    for i in range(n):
        print(i)
        print('index : ', index[indecies[i]], " score: ", scores[indecies[i]])
    # return indecies[:n]


def calculate_sim(user_profile, tfidf):
    for i in range(user_profile.shape[1]):
        scores = []
        index = []
        u = user_profile[:, i]
        for j in range(tfidf.shape[1]):
            v = tfidf[:, j]
            
            if np.linalg.norm(v.todense()) == 0:
                # 有一些新闻是空的，还没看到哪里出问题了
                # 只有个别的新闻是全英文所以没有关键词，其余的新闻还有一些是0
                continue
            
            tmp = sum(u.transpose().dot(v).todense()) / np.linalg.norm(u.todense()) / np.linalg.norm(v.todense())
            scores.append(np.array(tmp)[0][0])
            index.append(j)
        find_top_n_items(scores,index)


def main():
    user_ratings = [{0: 2.5, 1: 5, 2: 9, 3: 7,4: 5.5, 5: 9, 6: 10, 7: 4, 
                     8: 4, 9: 3, 10: 7, 11: 7, 12: 4, 13: 5, 14: 8, 15: 7, 
                     16: 6, 17: 7, 18: 4, 19: 3, 20: 3}]
    corpus = read_corpus()
    tmp_cor = corpus[0][0:500]
    for i in range(500):
        tmp_cor.append(corpus[1][i])
    
    tfidf = cal_tf_idf(tmp_cor)
    #print(tfidf)
    user_profile = gen_user_profile(tfidf, user_ratings)
    calculate_sim(user_profile, tfidf)


if __name__ == '__main__':
    main()
