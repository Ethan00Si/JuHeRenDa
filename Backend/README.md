# django
## apps
- recommender：推荐系统（已注册）

## mysql操作

- **在一个database中**

### 读取现有数据表
1. 在```/Backend/Dachaung/settings.py```中修改数据库名称、用户、密码，详见注释
2. ```cd /Backend/DaChuang```
3. ```python manage.py inspectdb > temporary.py```，该命令会在当前目录下生成```temporary.py```文件，此文件中存储着```settings.py```中定义的数据库的所有表对应的model类
3. 将需要的```class```复制到```/Backend/recommender/models.py```中
   - 如果同意使用django来接管该表的生命周期，将```class Meta```下的```managed```设置为```True```
4. ```python manage.py makemigrations```
5. ```python manage.py migrate recommender --fake```

### 创建新的数据表，详见[官方文档例子](https://docs.djangoproject.com/en/3.1/intro/tutorial02/#activating-models)
1. 声明新的数据表,
在```apps/models.py```中：
```python
    class x(models):
        #定义field
        #重写返回数据等函数
```
2. 将数据表注册到admin page，在
```apps/admin.py```中：
```python
    from .models import x
    admin.site.register(x)
```

3. 在```/Dachuang/Backend/```下运行：
    - ```python manage.py makemigrations recommender```：将改动存储到migrations，会在```/Dachuang/Backend/recommender/migrations/```下创建文件xxxx_initial.py，**xxxx即为该migration的名字**
    - ```python manage.py migrate recommender```应用改动

4. 查看对应的sql操作（**optional**）
  - 在```/Dachuang/Backend/```下运行：```python manage.py sqlmigrate recommender xxxx```，xxxx即为之前migration的名字

### 查找
- 详见[官方文档](https://docs.djangoproject.com/en/3.1/intro/tutorial02/#activating-models)
