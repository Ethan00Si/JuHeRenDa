# embedding相关

- ## dictinary.txt
  - 由/data/词典/ 下所有内容生成得到，用作jieba分词的用户词典（现有的6个学院除了法学院，剩下的都用到了）
  - 详见/data/词典/README.md
  

- ## stopList.txt
  - 停用词列表，网上找的，加入了自己定义的几个

- ## corpus_information.txt
  - 使用信息学院官网所有新闻和信火相传公众号及信息学院老师姓名、专业方向分词得到的语料库
  - 一行为一则新闻，已去除停用词（stopList.txt内容）
  - 并且根据用户词典dictionary.txt分词生成
  
- ## word_embeddings_information.model
  - word2vec根据corpus_information训练得到的模型

# TODO
1. 权衡stopList中的数字
2. 用户定义词典尚待完善（实验室、会议等等）


