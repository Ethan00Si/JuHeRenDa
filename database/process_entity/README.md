
major_in : -1
title_is : -2
position_is : -3
in : -4
work_in : -5

## 文件及功能
- process_to_neo.py 
  - 实现从raw_data处理后写入对应文件夹并更新字典的函数 process()
  - 实现将处理好的教师、实验室数据加入neo4j的函数 create_graph()

- utils.py
  - 实现将输入的从头开始的pandas的新闻中加入命名实体识后得到的新的dataframe（扩展了两列），将新加入的实体加入入entity_foreign.json
  - 在进行实体识别的过程中抽取关系，将关系应用到neo4j中。首先我们有句子中实体的id，那么对于某一个id，如果其 > GOLDEN_LENGTH，那么可以在entity_foreign中取得，应该说不用取。。。如果其小于GOLDEN_LENGTH，则根据id从neo4j中取得，之后如果加入人工校准等等涉及修改实体的功能，那么可以根据其id进行修改

## 要做的
- 识别信息学院、经济学院、教务处、信火相传的所有新闻的title的命名实体

## 问题
- 再添加实体时如何检查该实体是否已经在数据库中？ **done**
- 添加实验室 **done**
- 处理position，title，作为实体也构建到知识图谱里，**done**
- 爬数据
- 把create_teacher_node用@包裹起来
- 当有新数据时更新
- 同名的教师还无法处理