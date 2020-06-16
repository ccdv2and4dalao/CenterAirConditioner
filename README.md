
## CenterAirConditioner

+ 语言：Python
+ 框架：Flask

### Environment

+ Pycharm: 2019.3.3
+ Python: 3.7
+ Pip: 19.2.3
+ Docker: 19.03.11

### Database Specification

使用mysql公开发行的开源docker镜像，docker镜像版本号为：

```
# docker --version
Docker version 19.03.11, build 42e35e61f3
```

数据库Mysql镜像版本号为mysql:8.0，配置如下：

+ 字符集：utf8mb4
+ 数据库校对CI：utf8mb4_unicode_ci
+ environment:
      MYSQL_ROOT_PASSWORD: 12345678
      MYSQL_DATABASE: backend
      MYSQL_USER: madmin
      MYSQL_PASSWORD: 12345678

当镜像拉起后，将自动配置用户密码，并创建初始数据库backend，方便用户使用。


### Deployment

##### 直接运行在系统中

要求python版本至少为3.5，已经测试可用3.7版本运行。在根目录下执行，可拉起服务器：

```
python3 ./server_main.py --config /config.yaml --host 0.0.0.0 --port 2022
```

配置文件示例，具体规则可参考`abstract/component/configuration.py`中的Configuration类：

```
# do not push it to your repo!
database:
  connection-type: mysql
  user-name: madmin
  password: 12345678
  host:  10.233.234.3:3306
  database-name: backend
  charset: utf8mb4
  parse-time: true
  max-idle: 100
  max-active: 100
  escape: '`'
  location: Local

server:
  bcrypt-salt: '$2b$12$LJh77o2qdckmSf0kZNjude'

slave-default:
  metric-delay: 1000
  update-delay: 1000

admin:
  # echo Myriad-Dreamin | md5sum
  app-key: d9936b0cc6ede8388b0a47218ad11a26
  admin-password: ed99eebd-3857-45f1-b5a0-38c09c789232-66017e2c-f50c-414a-950a-f67405239b05
```

##### 使用docker运行

要求安装Docker较新版本（本次实验使用的版本号为19.03.11），并使用docker-compose拉起应用容器。

本实验编写了辅助部署的shell脚本，运行示例代码如下：

```
# ./bin/minimum # 进入运维虚拟环境
# xmake up
```

