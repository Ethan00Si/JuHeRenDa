import json

import numpy as np

from .user import ContentBased_User


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
        new_result.append(tmp[item])
    return new_result


def refresh_news(user_id):
    '''
    推荐新闻
    目前：
    1. 将tfidf存在本地
    2. keywords_list还未处理（留下user—id，希望以后可以从数据库中读取）
    3. user_profile, 目前直接将一个测试用的用户的画像保存在本地 profiles.npy
    4. 将用户所看过的新闻保存在本地，目前是already_views.json
    '''
    
    tfidf = np.load('recommender/CB/storage/tfidf.npy')
    tfidf = tfidf.T

    already_viewed_news = dict()
    with open('recommender/CB/storage/already_views.json', 'r') as fin:
        already_viewed_news = json.load(fin)

    user_profile = np.load('recommender/CB/storage/profiles.npy')
    user1 = ContentBased_User(
        key_words=['info'], profile=user_profile, already_view_news=already_viewed_news)
    # user1 = ContentBased_User(
    #     key_words=['info'], profile=np.zeros((tfidf.shape[0], 1)))

    # user1.generate_user_profile(tfidf, {0: -1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: -1, 8: -1, 9: -1, 10: 1},
    #                             ['recommender/CB/storage/profiles.npy', 'recommender/CB/storage/already_views.json'])
    # user1.update_user_profile(tfidf, {11: 1, 12: -1, 13: 1, 14: 1, 15: 1,
    #                                   16: 1, 17: 1, 18: -1, 19: -1, 20: -1})
    result = user1.generate_recommand(tfidf, 5)
    result = trans_lineID_to_artID(
        result, '../data/语料/cut_words_result/mapping.json')
    #print('dfghjhgfghjkjhghjk')
    return result


# refresh_news(1)
