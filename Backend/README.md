# django
## apps
- recommender：推荐系统（已注册）

## mysql操作

- **在一个database中（待研究）**

### 创建新的数据表，详见[官方文档例子](https://docs.djangoproject.com/en/3.1/intro/tutorial02/#activating-models)
- 声明新的数据表,
在```apps/models.py```中：
```python
    class x(models):
        #定义field
        #重写返回数据等函数
```
- 将数据表注册到admin page，在
```apps/admin.py```中：
```python
    from .models import x
    admin.site.register(x)
```

- 在```/Dachuang/Backend/```下运行：
    - ```python manage.py makemigrations recommender```：将改动存储到migrations，会在```/Dachuang/Backend/recommender/migrations/```下创建文件xxxx_initial.py，**xxxx即为该migration的名字**
    - ```python manage.py migrate recommender```应用改动

- 查看对应的sql操作（**optional**）
  - 在```/Dachuang/Backend/```下运行：```python manage.py sqlmigrate recommender xxxx```，xxxx即为之前migration的名字

### 查找
- 详见[官方文档](https://docs.djangoproject.com/en/3.1/intro/tutorial02/#activating-models)
