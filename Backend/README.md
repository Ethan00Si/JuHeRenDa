# django
##  1. <a name='apps'></a>apps
- recommender：推荐系统（已注册）
- search：搜索
- knoelwdge：知识库

# demo
## 功能
- recommender/urls.py中
  - 简单定义了推荐算法的url即```recommender/```
  - 简单定义了返回新闻的url即```recommender/art_id/```，以新闻编号作为携带的参数；
  
- recommender/views.py中
  - 定义了相应上述url即```recommender/```的函数，只是写了一行字，没加推荐算法的函数进来
  - 定义了响应上述url即```recommender/art_id/```的函数，以新闻编号```art_id```作为传入的值，实现查询该```art_id```的新闻，查询一系列新闻并返还到前端，该函数中**没有涉及增加数据项、删除数据项**，因为我认为暂时用不到，而且写出来会修改数据库中的数据，请谨慎
  - 支持使用sql语句操作
- recommender/templates/recommender/layout.html为html模板，用于展示返回到前端的值

## 使用方法

1. 在```/Backend/Dachaung/settings.py```中修改数据库名称、用户、密码，详见注释。注意数据库中必须已经建立了article、user_file、user_log、tfidf四个数据表，并且article数据表中有信息
2. ```shell
   cd /Backend
   ``` 
3. ```shell
   # 应用更改到django中
   python manage.py migrate recommender --fake
   ```
4. ```shell
   # 启动服务器
   python manage.py runserver
   ```
5. 访问[http://127.0.0.1:8000/recommender/1/](http://127.0.0.1:8000/recommender/11/)，其中1为新闻id，可以随意更改


# mysql操作

**在一个database中**
---

##  读取现有数据表
1. 在```/Backend/Dachaung/settings.py```中修改**数据库名称、用户、密码**，详见注释
2. ```
   cd /Backend
   ```
3. ```
   python manage.py inspectdb > temporary.py 
   ```
   - 该命令会在```/Backend```下生成```temporary.py```文件，此文件中存储着```settings.py```中定义的数据库的所有表对应的```model```类，将需要的类复制到```/Backend/recommender/models.py```中
     - 如果同意使用django来接管该表的生命周期，将```class Meta```下的```managed```设置为```True```

4. ```python
   # 将数据表的更改作为migration存储
   python manage.py makemigrations 
   ```
5. ```python
   # 应用更改到django中
   python manage.py migrate recommender --fake
   ```

##  创建新的数据表
1. 声明新的数据表,
在```apps/models.py```中：
```python
    class x(models):
        #定义field
        #重写返回数据等函数
```
1. 将数据表注册到admin page，在
```apps/admin.py```中：
```python
    from .models import x
    admin.site.register(x)
```

3. 在```/Dachuang/Backend/```下运行：
    - ```
       python manage.py makemigrations recommender
      ```
      将改动存储到migrations，会在```/Dachuang/Backend/recommender/migrations/```下创建文件xxxx_initial.py，**xxxx即为该migration的名字**
    - ```
       python manage.py migrate recommender
      ```
      应用改动

4. 查看对应的sql操作（**optional**）
     - 在```/Dachuang/Backend/```下运行：
      ```python
      python manage.py sqlmigrate recommender xxxx #xxxx为migration的名字
      ```

5. 详见[官方文档例子](https://docs.djangoproject.com/en/3.1/intro/tutorial02/#activating-models)
  
---
## 查找
```python
from .models import x
x.objects.get(pk=xxx)                   #返回单个数据，不能找多个
x.objects.filter(Field_1__gt=1)      #返回多个数据，lookup方法有很多 
```
- ### 查找的各种方法详见[官方文档](https://docs.djangoproject.com/en/3.1/topics/db/queries/#field-lookups-intro)
- ### [内置lookup](https://docs.djangoproject.com/en/3.1/ref/models/querysets/#field-lookups)
---
## 向数据库中添加数据
- 直接添加
    ```python
    from .models import x
    x.objects.create(Field_1="var_field_1",Field_2="var_field_2"...)
    ```
- 声明实例，之后保存
    ```python
    from .models import x
    my_x = x(Field_1="var_field_1",Field_2="var_field_2"...)
    my_x.save()
    ```
- #### 详见[官方文档](https://docs.djangoproject.com/en/3.1/ref/models/instances/)

## 从数据库中删除数据
```python
from .models import x
to_delete = x.objects.filter(pk__gt=10)     #返回pk大于10的子集
to_delete.delete()                          #直接从数据库中删除，但python实例仍然存在，其中数据已经被删除
to_delete[0]                                #IndexError
```
- ### [自定义删除的方法](https://docs.djangoproject.com/en/3.1/topics/db/queries/#topics-db-queries-delete)
---
## 更多
- ### django可以用普通sql语句，[文档](https://docs.djangoproject.com/en/3.1/topics/db/sql/)

- ### 用解决多个线程往数据库中写入，[文档](https://docs.djangoproject.com/en/3.1/ref/models/expressions/)

- ### [django数据库优化访问方式概览](https://docs.djangoproject.com/en/3.1/topics/db/optimization/)

- ### [cache](https://docs.djangoproject.com/en/3.1/topics/cache/#the-per-site-cache)

***

# utl操作

## 注册url
1. 在DaChuang.urls中注册
2. 在每个apps.urls中注册，并且加入app_name
3. url中的变量名和view的变量名必须一致
4. 在模板中访问url别忘了加app名，'url' xx:yy

## [自定义filter,tags](https://docs.djangoproject.com/en/3.1/howto/custom-lookups/)
