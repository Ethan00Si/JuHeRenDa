import torch
import torch.nn as nn
import fm

class FM_user():
    def __init__(self):
        self.FM = self.load_FM()
        # 保留接口
        # self.newsID_list = self.get_newsID_list()
        # self.index2newsID = self.create_index2newsID()
        self.X = self.create_X()

    def load_FM(self):
        '''读入保存的FM模型'''
        # 模型储存的地址
        path = r'recommend_system\fm_params.pt'
        # 新建FM模型，暂时先用n、k来代替
        # 测试用的n=10810 k=5
        FM = fm.FM(10810, 5)
        # 读入参数
        FM.load_state_dict(torch.load(path))

        return FM

    def predict(self, X):
        '''输入构造好的特征向量，进行预测'''
        # 以后应该会加上try/except
        # predict
        y = self.FM(X)
        return y

    def get_newsID_list(self):
        '''粗筛选得到待推荐的新闻'''
        # 与数据库交互 去重

        return newsID_list

    def create_index2newsID(self):
        '''构建index与新闻的映射表'''
        index2newsID = dict()
        for index, newsID in enumerate(self.newsID_list):
            index2newsID.update({index: newsID})
        return index2newsID

    def create_X(self):
        '''根据新闻列表构造待预测特征向量'''
        # 目前采用读一行数据进来的方法模拟构建的特征向量
        with open(r'recommend_system\模拟特征向量.txt', 'r') as f:
            
            lines = f.readlines()
        X = [float(x) for x in lines]
        X = torch.tensor([X])
        X = X.clone().detach().float()
        return X

    def my_sort(self, y):
        '''为预测结果排序，返回为(index, newsID, value)'''

        return results


    def recommend(self):
        '''推荐的主函数'''
        # 预测
        y = self.predict(self.X)
        # 排序 目前因为测试的特征向量直接1条 因此不排序
        # results = self.my_sort(y)
        # 测试用 只返回一个预测值
        return y

if __name__ == "__main__":
    user = FM_user()
    y = user.recommend()
    print(y)
        
