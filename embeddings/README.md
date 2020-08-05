# 训练word2vec，保存训练模型

## 目录结构
D:.
│  embedding.py             //定义一些训练时候处理数据的函数
│  README.md                
│  test_word2vec.ipynb      //训练word2vec
│
└─__pycache__

## embedding.py中定义函数
- mergeDict：遍历/data/字典 目录下所有的.txt文件，将其合并为一个大字典（不重复）
- getStopList：获取停用词列表
- getDict：获取大字典
- getCorpus：读取语料库