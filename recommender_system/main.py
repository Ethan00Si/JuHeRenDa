import feature_matrix
from user import ContentBased_User
import numpy as np

tfidf, vocabulary = feature_matrix.gen_matrix() #返回的tfidf是用csr存储的稀疏矩阵
'''
news = feature_matrix.read_corpus()
tfidf = feature_matrix.update_matrix(vocabulary,tfidf,news[0][:500])
print( (tfidf.toarray()[:,0]==tfidf.toarray()[:,1000]).all() )
np.set_printoptions(suppress=True)
print(tfidf.toarray()[:,0])
print(tfidf.toarray()[:,1000])
'''
user1 = ContentBased_User(key_words=['info'],profile= np.ndarray((tfidf.shape[0], 1) ))

user1.generate_user_profile(tfidf, {0: -1, 1: 1, 2: 1, 3: 1,4: 1, 5: 1, 6: 1, 7: -1, 8: -1, 9: -1, 10: 1})
user1.update_user_profile(tfidf, {11: 1, 12: -1, 13: 1, 14: 1, 15: 1, 
                     16: 1, 17: 1, 18: -1, 19: -1, 20: -1})
user1.generate_recommand(tfidf, 10)

