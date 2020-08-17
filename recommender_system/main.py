from feature_matrix import gen_matrix
from user import ContentBased_User
import numpy as np

tfidf = gen_matrix()

user1 = ContentBased_User(key_words=['info'],profile= np.ndarray((tfidf.shape[0], 1) ))

user1.generate_user_profile(tfidf, {0: 2.5, 1: 5, 2: 9, 3: 7,4: 5.5, 5: 9, 6: 10, 7: 4, 8: 4, 9: 3, 10: 7})
user1.update_user_profile(tfidf, {11: 7, 12: 4, 13: 5, 14: 8, 15: 7, 
                     16: 6, 17: 7, 18: 4, 19: 3, 20: 3})
user1.generate_recommand(tfidf, 10)
