
基于Django的新正方教务管理系统的爬虫webApi，请求**返回JSON数据**
部分本地API基于[NeroAsmarr/zfnew][1](2020.2.16)

## 使用方法

### Tips

 - 通过pinfo新增学生，并将cookies存入数据库
 - 请求其它内容时，cookies失效后再重新执行登录，并更新数据库中的cookies
 - 选课API可能并不通用，这里仅提供思路，具体请参照自己学校情况
 - 鉴于实现方式和并发量，并不建议将本项目部署到产品项目中
 - CentOs自带的sqlite3版本较低，Django2.1.8以上不兼容
     - 解决办法一：通过requirements.txt安装模块，在requirements.txt中的Django版本已经更改为为2.1.8
     - 解决办法二：升级自带的sqlite3版本，并重新链接（移步百度

### POST地址&Data

#### 请求信息
```
个人信息(必须，用以登录)：http://xxx:8000/info/pinfo
信息FromData={xh:'学号',pswd:'密码'}
停补换课消息：http://xxx:8000/info/message
消息FromData={xh:'学号',pswd:'密码'}
课程修读情况(学业详情)：http://xxx:8000/info/study
学业FromData={xh:'学号',pswd:'密码'}
请求成绩: http://xxx:8000/info/grade
成绩FromData={xh:'学号',pswd:'密码',year:'查询学年',term:'查询学期'}
请求课表：http://xxx:8000/info/schedule
课表FromData={xh:'学号',pswd:'密码',year:'查询学年',term:'查询学期'}
手动更新cookies：http://xxx:8000/info/update
更新FromData={xh:'学号',pswd:'密码'}
```
#### 选课请求
```
请求已选课程：http://xxx:8000/choose/choosed
已选FromData={xh:'学号',pswd:'密码'}
板块课：http://xxx:8000/choose/bkk
板块课FromData={xh:'学号',pswd:'密码',bkk:'1 or 2'}
(Todo)选择某课：http://xxx:8000/choose/confirm
选课FromData={xh:'学号',pswd:'密码',id:'教学班ID'}
(Todo)退掉某课：http://xxx:8000/choose/cancel
退课FromData={xh:'学号',pswd:'密码',id:'教学班ID'}
```

## 使用部署
 - 推荐使用**uswgi+nginx**，具体部署可移步百度

## 测试部署(建议仅测试用)

 - 请确保服务器或虚拟环境安装了**Python3.6**及以上版本

### 1.安装依赖模块

```shell
$ pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### 2.开放安全组配置
 - 开放80、8000端口

### 3.用终端打开zfnweb文件夹，并运行

```shell
$ python manage.py runserver 0.0.0.0:8000
```

访问你服务器的**IP地址:8000**

  [1]: https://github.com/NeroAsmarr/zfnew