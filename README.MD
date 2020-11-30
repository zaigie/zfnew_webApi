
⭐新正方教务管理系统的爬虫webApi-Django(带后台)🔧用以开发校园APP/小程序

**登录、消息及成绩和课程**部分API基于[NeroAsmarr/zfnew](https://github.com/NeroAsmarr/zfnew)【2020.2.16】

目前项目部署在“西院助手”微信/QQ小程序中作为API

求⭐⭐⭐⭐⭐（跪

 - [相关说明](#相关说明)
    - [功能实现](#功能实现)
    - [返回数据内容说明](#返回数据内容说明)
    - [Tips](#Tips)
 - [接口](#接口)
    - [信息请求](#信息请求)
    - [选课请求](#选课请求)
    - [其它请求](#其它请求)
 - [使用部署](#使用部署)
 - [测试部署](#测试部署-测试用)

------

## 相关说明

### 功能实现

 - [x] 个人信息
 - [x] 停补换课消息
 - [x] 课程修读情况(学业详情)
 - [x] 成绩
 - [x] 课表
 - [x] 查询已选课程
 - [x] 选课
 - [x] 退课
 - [x] 录取查询(仅本校)
 - [ ] 空教室查询

------

 - [x] 响应式后台管理数据库
 - [x] 对每天的每个请求生成日志文件
 - [x] 避免教务系统无法访问，存储部分请求数据到服务器，可选参数刷新
 - [x] 查询各院/专业/班级加入情况
 - [x] 查询GPA在专业与班级的排名

### 返回数据内容说明

 - 点击[JSON说明.MD](https://github.com/jokerwho/zfnew_webApi/blob/master/JSON说明.MD)访问返回的JSON数据键值名称以及具体内容说明

### Tips

 - 为了方便管理和请求，不采用传递cookies的方法，而是**将cookies存储到数据库**让服务器请求
 - 须先通过pinfo新增学生后才能访问其它API
 - 使用simpleui后台，自定义在**settings.py**以及**info/admin.py**和**info/models.py**
 - 选课API可能**并不通用**，这里仅提供思路，具体请参照自己学校情况
 - 代码中有关于开发者本校的**录取查询(recruitApp)**，**不通用**，请自行编写替换或删除
 - 使用MySQL数据库，请保证MySQL版本为**5.6及以上**
 - **config.json**中包含了http代理、官网、Server酱、上下课时间配置
    - ServerChan为**none**时，不使用Server酱，而配置时须填上完整url，**末尾以'.send?'结尾**
    - proxy为**none**时，不使用代理
    - nowterm本来想写成自动判断的，但想到第一个期末成绩出来的时间不定，所以还是用了手动配置，'3'为上学期，'12'为下学期

## 接口

### 信息请求

------

**个人信息(必须，用以登录)：/info/pinfo**
参数名 | 必选 |  说明  
-|-|-
xh | 是 | 学号 |
pswd | 是 | 密码 |

**停补换课消息：/info/message**
参数名 | 必选 |  说明  
-|-|-
xh | 是 | 学号 |
pswd | 是 | 密码 |

**课程修读情况(学业详情)：/info/study**
参数名 | 必选 |  说明  
-|-|-
xh | 是 | 学号 |
pswd | 是 | 密码 |
refresh | 否 | 填入'no'则读取缓存 |

**成绩: /info/grade**
参数名 | 必选 |  说明  
-|-|-
xh | 是 | 学号 |
pswd | 是 | 密码 |
year | 是 | 学年 |
term | 是 | 学期(1 or 2) |
refresh | 否 | 填入'no'则读取缓存 |

**课表：/info/schedule**
参数名 | 必选 |  说明  
-|-|-
xh | 是 | 学号 |
pswd | 是 | 密码 |
year | 是 | 学年 |
term | 是 | 学期(1 or 2) |
refresh | 否 | 填入'no'则读取缓存 |

**查询各院/专业/班级加入情况：/info/joindetail**
**方法：GET**
参数名 | 必选 |  说明  
-|-|-
type | 是 | college-二级学院,major-专业,class-班级 |

**查询GPA在专业与班级的排名：/info/position**
**方法：GET**
参数名 | 必选 |  说明  
-|-|-
xh | 是 | 学号 |

------

### 选课请求

------

**已选课程：/choose/choosed**
参数名 | 必选 |  说明  
-|-|-
xh | 是 | 学号 |
pswd | 是 | 密码 |
refresh | 否 | 填入'no'则读取缓存 |

**板块课：/choose/bkk**
参数名 | 必选 |  说明  
-|-|-
xh | 是 | 学号 |
pswd | 是 | 密码 |
bkk | 是 | 板块号(1 or 2) |

**选课：/choose/choose**
参数名 | 必选 |  说明  
-|-|-
xh | 是 | 学号 |
pswd | 是 | 密码 |
doId | 是 | 执行ID，精确到班级，从板块课API中可获取 |
kcId | 是 | 课程号，精确到课程，从板块课API中可获取，在其它API中字段名为"**courseId**" |
kklxdm | 是 | 精确到板块课页面，从板块课API中可获取，板块课1、2不同 |

**退课：/choose/cancel**
参数名 | 必选 |  说明  
-|-|-
xh | 是 | 学号 |
pswd | 是 | 密码 |
doId | 是 | 执行ID，精确到班级，从板块课API中可获取 |
kcId | 是 | 课程号，精确到课程，从板块课API中可获取，在其它API中字段名为"**courseId**" |

------

### 其它请求

------

**one·一个 每日文字：/one**

※method : GET

**录取查询（仅作者学校）：/recruit/query**
参数名 | 必选 |  说明  
-|-|-
identity | 是 | 考生号 or 身份证号 |

------

## 使用部署
 - 推荐使用**uswgi+nginx**，具体部署可移步百度
 - 更改config.json中各项：参照上方Tips

## 测试部署-测试用

 - 请确保服务器或虚拟环境安装了**Python3.6**及以上版本

### 1.安装依赖模块

```shell
$ pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### 2.开放安全组配置
 - 开放8000端口

### 3.使用-迁移数据库

 - 在settings.py中配置数据库信息

```shell
$ python manage.py makemigrations
$ python manage.py migrate
```

### 4.创建后台用户

```shell
$ python manage.py createsuperuser
```

### 5.用终端打开zfnweb文件夹，并运行

```shell
$ python manage.py runserver 0.0.0.0:8000
```

### 6.访问后台

```
/admin
```

访问你服务器的**IP地址:8000/xxx**