from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix
import numpy as np

'''
基于内容的推荐，对于每一个用户来说，所需要推荐的内容都是不一样的，
所以可以考虑类是以用户为单位的，
考虑到tf-idf矩阵是一个公共的数据，所有人都要用
'''


class ContentBased_User(object):
    '用户的基于内容推荐的基类'
    users_cnt = 0  # 用户数量

    def __init__(self, key_words, profile):
        self.key_word_list = key_words  # 用户的关键词列表
        self.user_profile = profile # 此用户的用户画像

    def generate_user_profile(self, tfidf, user_ratings):
        # 这里的user_ratings是以dict的形式存储 格式 doc ID : score
        # 生成用户画像
        user_profile = np.ndarray((tfidf.shape[0], 1))
        '''
        假定大于0是喜欢 小于0是不喜欢，数据是已经预处理好的
        '''
        # rocchio algorithm 一般设置 a = 1,b = 0.8, c = 0.1
        b = 0.8
        c = 0.1
        threshold_rate = 1e-10
        tf_idf_matrix = tfidf.toarray()
        
        pos_cnt = 0
        neg_cnt = 0
        '''
        下面这里没有想好相关的新闻和不相关的新闻如何影响user profile，暂定是乘得分作为影响
        '''
        for item in user_ratings:
            if(user_ratings[item] > 0):
                pos_cnt += 1
        for item in user_ratings:
            if(user_ratings[item] < 0):
                neg_cnt += 1

        for item in user_ratings:
            if(user_ratings[item] >= 0):
                user_profile[:, 0:1] += b/pos_cnt * tf_idf_matrix[0:, item:item+1]
                
        for item in user_ratings:
            if(user_ratings[item] < 0):
                user_profile[:, 0:1] -= c/neg_cnt * tf_idf_matrix[0:, item:item+1]
                    
        (rows, cols) = user_profile.shape
        
        for i in range(rows):
            for j in range(cols):
                if(user_profile[i, j] < threshold_rate and user_profile[i, j] > -threshold_rate):
                    user_profile[i, j] = 0
        
        
        user_profile = csr_matrix(user_profile)
        
        '''
                    user
          vocabulary|--|
                    |  |
        metric:     |  |
                    |  |
                    |--|  
        '''
        self.user_profile = user_profile


    def update_user_profile(self, tfidf, user_ratings):
        # 新增加了一些评价，更新用户画像

        b = 0.8
        c = 0.1
        
        tf_idf_matrix = tfidf.toarray()

        pos_cnt = 0
        neg_cnt = 0
        '''
        下面这里没有想好相关的新闻和不相关的新闻如何影响user profile，暂定是乘得分作为影响
        '''
        for item in user_ratings:
            if(user_ratings[item] > 0):
                pos_cnt += 1
        for item in user_ratings:
            if(user_ratings[item] < 0):
                neg_cnt += 1

        for item in user_ratings:
            if(user_ratings[item] >= 0):
                self.user_profile[:, 0:1] += b/pos_cnt * tf_idf_matrix[0:, item:item+1]
                
        for item in user_ratings:
            if(user_ratings[item] < 0):
                self.user_profile[:, 0:1] -= c/neg_cnt * tf_idf_matrix[0:, item:item+1]

    def generate_recommand(self, tfidf, topN = 10):
        #  产生推荐结果
        for i in range(self.user_profile.shape[1]):
            scores = []
            index = []
            u = self.user_profile[:, i]
            for j in range(tfidf.shape[1]):
                v = tfidf[:, j]
                
                if np.linalg.norm(v.todense()) == 0:
                    # 有一些新闻是空的，还没看到哪里出问题了
                    # 只有个别的新闻是全英文所以没有关键词，其余的新闻还有一些是0
                    continue
                
                tmp = sum(u.transpose().dot(v).todense()) / np.linalg.norm(u.todense()) / np.linalg.norm(v.todense())
                scores.append(np.array(tmp)[0][0])
                index.append(j)
        self.find_top_n_items(scores, index, topN)

    def find_top_n_items(self, scores, index, n):
        # 输出前n个结果
        print("max: ",max(scores))
        scores = np.array(scores)
        indecies = np.argsort(-scores)
        for i in range(n):
            print(i)
            print('index : ', index[indecies[i]], " score: ", scores[indecies[i]])
        # return indecies[:n]