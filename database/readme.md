# 创建数据库

* 首先，在服务器上创建一个数据库，名字为Dachuang

  ```sql
  CREATE DATABASE Dachuang;
  ```

* 修改database.py中 登陆mysql的用户名和密码

* 先把construct_tables运行一遍，注释掉insert_to_article

  * ==运行位置==：由于相对路径是基于当前路径在DaChuang文件下所写的，所以运行时在DaChuang文件下运行

    ```shell
    python3 database/database.py
    ```

    

* 运行insert_to_article，注释掉construct_tables

