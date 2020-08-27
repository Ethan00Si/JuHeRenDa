# FM的说明文档

last update time: 20200827

## 文件结构

```
.
├── ./README.md
├── ./fm.py
├── ./fm_params.pt
├── ./fm_user.py
└── ./模拟特征向量.txt

0 directories, 5 files
```

## 文件说明

fm.py：用pytorch写的FM类

fm_user.py：针对一个用户写的类

fm_params.pt：已经训练好的FM模型，数据集为movielens数据集

模拟特征向量.txt：因为现在没有实际数据，因此用了movielens的数据。内行一条特征向量