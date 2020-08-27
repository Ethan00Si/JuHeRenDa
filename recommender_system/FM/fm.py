import torch
import torch.nn as nn


class FM(nn.Module):
    def __init__(self, n, k):
        super(FM, self).__init__()
        # 输入的特征向量的维度
        self.n = n
        # 矩阵V隐含层的维度，越大越过拟合，越小越欠拟合
        self.k = k
        # 前两项线性项
        self.linear = nn.Linear(self.n, 1)
        # 将矩阵V加入参数中
        self.V = nn.Parameter(torch.randn(self.n, self.k))
    
    def forward(self, x):
        # 线性项
        linear_part = self.linear(x)
        # 交叉项
        inter_part1 = torch.pow(torch.mm(x, self.V), 2)
        inter_part2 = torch.mm(torch.pow(x, 2), torch.pow(self.V, 2))
        # 化简后时间复杂度为O(kn)的公式
        # sum后要将维度变为1，不然batch训练时不收敛
        output = linear_part + 0.5 * torch.sum(inter_part1 - inter_part2, 1)
        return output



