from .user import ContentBased_User
import numpy as np
import json

def trans_lineID_to_artID(result, mapping_path):
    """
    将返回的tf-idf的行号转换成数据库article中的art_ID
    parameters:
    1. result 计算返回的前5个匹配结果的结果的tfidf的行号
    2. mapping_path tfidf行与article中的新闻的对应关系
    """
    mapping = dict()
    with open(mapping_path, 'r') as fin:
        mapping = json.load(fin)
    tmp = dict()
    for item in mapping:
        tmp[mapping[item]] = item

    new_result = list()
    for item in result:
        new_result.append(str(int(tmp[item])-81125+4857))
    return new_result

def refresh_news(user_id):

    tfidf = np.load('recommender/CB/storage/tfidf.npy')

    tfidf = tfidf.T
    user1 = ContentBased_User(key_words=['info'], profile=np.ndarray((tfidf.shape[0], 1)))

    # user1.generate_user_profile(
    #     tfidf, {0: -1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: -1, 8: -1, 9: -1, 10: 1})
    # user1.update_user_profile(tfidf, {11: 1, 12: -1, 13: 1, 14: 1, 15: 1,
    #                                     16: 1, 17: 1, 18: -1, 19: -1, 20: -1})
    result = user1.generate_recommand(tfidf, 5)
    result = trans_lineID_to_artID(
        result, '../data/语料/cut_words_result/mapping.json')

    return result