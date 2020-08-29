# createNode.py
- 输入：无（默认获取处理后的教师数据）
- 输出：将教师节点存入neo4j

major_in : -1
title_is : -2
position_is : -3
in : -4
work_in : -5

# 问题
- 再添加实体时如何检查该实体是否已经在数据库中？ **done**
- 添加实验室 **done**
- 处理position，title，作为实体也构建到知识图谱里，**done**
- 爬数据
- 把create_teacher_node用@包裹起来
- 对比知识库进行实体识别