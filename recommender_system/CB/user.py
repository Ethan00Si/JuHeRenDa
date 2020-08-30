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
        self.already_view = dict() #已经浏览过的页面,dict是哈希表，O(1)复杂度

    def generate_user_profile(self, tfidf, user_ratings):
        # 将已经看过的内容添加到 already_view中
        for item in user_ratings:
            self.already_view[item] = 1


        # 这里的user_ratings是以dict的形式存储 格式 doc ID : score
        # 生成用户画像
        user_profile = np.zeros((tfidf.shape[0], 1))
        '''
        假定大于0是喜欢 小于0是不喜欢，数据是已经预处理好的
        '''
        # rocchio algorithm 一般设置 a = 1,b = 0.8, c = 0.1
        b = 0.8
        c = 0.1
        threshold_rate = 1e-10
        
        pos_cnt = 0
        neg_cnt = 0
        '''
        下面这里没有想好相关的新闻和不相关的新闻如何影响user profile，暂定是乘得分作为影响
        '''
        for item in user_ratings:
            if(user_ratings[item] >= 0):
                pos_cnt += 1
        for item in user_ratings:
            if(user_ratings[item] < 0):
                neg_cnt += 1

        for item in user_ratings:
            if(user_ratings[item] >= 0):
                user_profile[:, 0] += b/pos_cnt * tfidf[:, item]
                
        for item in user_ratings:
            if(user_ratings[item] < 0):
                user_profile[:, 0] -= c/neg_cnt * tfidf[:, item]
                    
        (rows, cols) = user_profile.shape
        
        '''
                    user
          vocabulary|--|
                    |  |
        metric:     |  |
                    |  |
                    |--|  
        '''
        self.user_profile = user_profile
        self.user_profile[np.isnan(self.user_profile)] = 0

    def update_user_profile(self, tfidf, user_ratings):
        # 添加已经看了的内容
        for item in user_ratings:
            self.already_view[item] = 1

        # 新增加了一些评价，更新用户画像

        b = 0.8
        c = 0.1

        pos_cnt = 0
        neg_cnt = 0
        '''
        下面这里没有想好相关的新闻和不相关的新闻如何影响user profile，暂定是乘得分作为影响
        '''
        for item in user_ratings:
            if(user_ratings[item] >= 0):
                pos_cnt += 1
        for item in user_ratings:
            if(user_ratings[item] < 0):
                neg_cnt += 1

        for item in user_ratings:
            if(user_ratings[item] >= 0):
                self.user_profile[:, 0] += b/pos_cnt * tfidf[:, item]
                
        for item in user_ratings:
            if(user_ratings[item] < 0):
                self.user_profile[:, 0] -= c/neg_cnt * tfidf[:, item]
        self.user_profile[np.isnan(self.user_profile)] = 0

    def generate_recommand(self, tfidf, topN = 10):
        #  产生推荐结果
        
        for i in range(self.user_profile.shape[1]):
            scores = []
            index = []
            u = self.user_profile[:, i:i+1]
            for j in range(tfidf.shape[1]):
                v = tfidf[:, j:j+1]
                
                if np.linalg.norm(v) == 0:
                    # 有一些新闻是空的，还没看到哪里出问题了
                    # 只有个别的新闻是全英文所以没有关键词，其余的新闻还有一些是0
                    continue
                tmp = np.dot(u.T,v) / np.linalg.norm(u) / np.linalg.norm(v)
                scores.append(tmp[0][0]) # score list存储每一个新闻的预测得分
                index.append(j)
        self.find_top_n_items(scores, index, topN)
        
    def find_top_n_items(self, scores, index, n):
        # 输出前n个结果
        print("max: ",max(scores))
        scores = np.array(scores)
        indecies = np.argsort(-scores)
        cnt = 0
        i = 0
        while(cnt < n):
            # 排除掉已经看过的新闻
            if self.already_view.__contains__(index[indecies[i]]):
                i += 1
                continue
            
            print(cnt)
            print('index : ', index[indecies[i]], " score: ", scores[indecies[i]])
            i += 1
            cnt += 1
        