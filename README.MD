
基于Django+MySQL的新正方教务管理系统的爬虫webApi(带后台)

**登录、消息及成绩和课程**部分API基于[NeroAsmarr/zfnew](https://github.com/NeroAsmarr/zfnew)【2020.2.16】

目前项目部署在“西院助手”微信/QQ小程序中作为API

求⭐⭐⭐⭐⭐（跪

## 使用方法

### JSON数据键值参照

 - 点击[JSON键值](#JSON键值)访问返回的JSON数据键值名称参照

### Tips

 - 由于学校教务系统可能会不定期无法访问，所以将学生请求到的信息以json格式分类存储到服务器
 - 为了方便管理和请求，不采用传递cookies的方法，而是**将cookies存储到数据库**让服务器请求
 - 须先通过pinfo新增学生后才能访问其它API
 - 使用simpleui后台，自定义在**settings.py**以及**info/admin.py**和**info/models.py**
 - 请求其它内容时，cookies失效后将重新执行登录，并更新数据库中的两个cookies字段和updateTime字段以及增加refreshTimes次数字段（请求内容失败可能并不完全是因为cookies失效，但目前暂未遇到其它错误，且更新cookies也是一个较为通用的解决办法）
 - 选课API可能**并不通用**，这里仅提供思路，具体请参照自己学校情况
 - 代码中有关于开发者本校的**录取查询(recruitApp)**，**不通用**，请自行编写替换或删除
 - 使用MySQL数据库，请保证MySQL版本为**5.6及以上**
 - **config.json**中包含了http代理、官网、Server酱、上下课时间配置
    - ServerChan为**none**时，不使用Server酱，而配置时须填上完整url，**末尾以'.send?'结尾**
    - proxy为**none**时，不使用代理
    - nowterm本来想写成自动判断的，但想到第一个期末成绩出来的时间不定，所以还是用了手动配置，'3'为上学期，'12'为下学期

### POST地址&Data
#### 请求信息
```
个人信息(必须，用以登录)：/info/pinfo
※信息参数={xh:'学号',pswd:'密码'}

停补换课消息：/info/message
※消息参数={xh:'学号',pswd:'密码'}

课程修读情况(学业详情)：/info/study
※学业参数={xh:'学号',pswd:'密码',refresh:'是否刷新(no/yes)'}

请求成绩: /info/grade
※成绩参数={xh:'学号',pswd:'密码',year:'查询学年',term:'查询学期',refresh:'是否刷新(no/yes)'}

请求课表：/info/schedule
※课表参数={xh:'学号',pswd:'密码',year:'查询学年',term:'查询学期',refresh:'是否刷新(no/yes)'}

手动更新cookies：/info/update
※更新参数={xh:'学号',pswd:'密码'}
```
#### 选课请求
```
请求已选课程：/choose/choosed
※已选参数={xh:'学号',pswd:'密码',refresh:'是否刷新(no/yes)'}

板块课：/choose/bkk
板块课参数={xh:'学号',pswd:'密码',bkk:'1 or 2'}

选择某课：/choose/choose
※选课参数={xh:'学号',pswd:'密码',doId:'执行ID',kcId:'课程号',kklxdm:'板块课1/2特有ID'}

退掉某课：/choose/cancel
※退课参数={xh:'学号',pswd:'密码',doId:'执行ID',kcId:'课程号'}
```

### 额外请求
```
one·一个 每日文字：/one
※GET请求

录取查询（通过开发者所在学校招生网获取数据，不通用）：/recruit/query
※录取参数={identity:'考生号' or '身份证号'}
```

## 使用部署
 - 推荐使用**uswgi+nginx**，具体部署可移步百度
 - 更改config.json中各项：参照上方Tips

## 测试部署(建议仅测试用)

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

# JSON键值

## 个人信息（登录）

```json
{
    "name": "学生姓名",
    "studentId": "学生学号",
    "birthDay": "出生日期",
    "idNumber": "身份证号码",
    "candidateNumber": "考生号",
    "status": "在读情况",
    "collegeName": "所在院系",
    "majorName": "所在专业",
    "className": "所在班级",
    "entryDate": "入学时间",
    "graduationSchool": "毕业高中",
    "domicile": "籍贯",
    "phoneNumber": "电话号码",
    "parentsNumber": "家长号码",
    "email": "电子邮箱",
    "politicalStatus": "政治面貌",
    "national": "民族",
    "education": "学历",
    "postalCode": "邮编",
    "grade": "年级"
}
```

## 学业情况

```json
{
    "gpa":"平均学分绩点GPA",
    "ipa":"计划内总课程数",
    "ipp":"计划内已过课程数",
    "ipf":"计划内未过课程数",
    "ipn":"计划内未修课程数",
    "ipi":"计划内在读课程数",
    "opp":"计划外已过课程数",
    "opf":"计划外未过课程数",
    "tsData":{
        "tsPoint":{
            "tsr":"通识教育要求学分",
            "tsg":"通识教育已得学分",
            "tsn":"通识教育未得学分",
        },
        "tsItems":[{
            "courseTitle":"课程名程",
            "courseId":"课程号",
            "courseSituation":"修读状态",
            "courseTerm":"修读学期",
            "courseCategory": "课程类别",
            "courseAttribution": "课程性质",
            "maxGrade":"最高成绩",
            "credit":"课程学分",
            "gradePoint":"课程绩点",
        }],
        },
    "tzdata":{
        "tzPoint":{
            "tzr":"拓展教育要求学分",
            "tzg":"拓展教育已得学分",
            "tzn":"拓展教育未得学分",
        },
        "tzItems":[{
            "courseTitle":"课程名程",
            "courseId":"课程号",
            "courseSituation":"修读状态",
            "courseTerm":"修读学期",
            "courseCategory": "课程类别",
            "courseAttribution": "课程性质",
            "maxGrade":"最高成绩",
            "credit":"课程学分",
            "gradePoint":"课程绩点",
        }],
        },
    "zydata":{
        "zyPoint":{
            "zyr":"专业教育要求学分",
            "zyg":"专业教育已得学分",
            "zyn":"专业教育未得学分",
        },
        "zyItems":[{
            "courseTitle":"课程名程",
            "courseId":"课程号",
            "courseSituation":"修读状态",
            "courseTerm":"修读学期",
            "courseCategory": "课程类别",
            "courseAttribution": "课程性质",
            "maxGrade":"最高成绩",
            "credit":"课程学分",
            "gradePoint":"课程绩点",
        }],
        },
    "qtdata":{
        "qtPoint":"{其它课程一般无学分要求}",
        "qtItems":[{
            "courseTitle":"课程名程",
            "courseId":"课程号",
            "courseSituation":"修读状态",
            "courseTerm":"修读学期",
            "courseCategory": "课程类别",
            "courseAttribution": "课程性质",
            "maxGrade":"最高成绩",
            "credit":"课程学分",
            "gradePoint":"课程绩点",
        }],
        },
}
```

## 停补课消息

```json
[
    {
        "message": "消息内容", 
        "ctime": "消息创建时间"
    }
]
```

## 成绩信息

```json
{
    "name": "学生姓名",
    "studentId": "学生学号",
    "schoolYear": "查询学年",
    "schoolTerm": "查询学期",
    "course": [{
        "courseTitle": "课程名程",
        "teacher": "课程老师",
        "courseId": "课程号",
        "className": "教学班名称",
        "courseNature": "课程性质",
        "credit": "课程学分",
        "grade": "课程成绩",
        "gradePoint": "课程绩点",
        "gradeNature": "考试性质",
        "startCollege": "授课院系",
        "courseMark": "主/选修",
        "courseCategory": "课程类别",
        "courseAttribution": "课程方向"
    }]
}
```

## 课表信息
```json
{
    "name": "学生姓名",
    "studentId": "学生学号",
    "schoolYear": "查询学年",
    "schoolTerm": "查询学期",
    "normalCourse": [{
        "courseTitle": "课程名程",
        "courseTitleShort":"课程短名称(超过x个字符显示省略号)",
        "teacher": "课程老师",
        "courseId": "课程号",
        "courseWeekday":"星期几",
        "courseSection": "课程节数",
        "includeSection": "该课程所在节数列表",
        "upTime": "课程上课时间",
        "courseTime":"课程时间",    #根据config.json里面的TimesUp和TimesDown
        "courseWeek": "课程周数",
        "includeWeeks":"该课程所在周数列表",
        "exam":"考试性质",
        "campus": "上课校区",
        "courseRoom": "上课地点",
        "className": "教学班名称",
        "hoursComposition": "学时",
        "weeklyHours": "周学时",
        "totalHours": "总学时",
        "credit": "课程学分"
    }],
}
```

## 已选课程

```json
{
    "courseNumber":"已选课程数",
    "items":[{
        "courseTitle":"课程名程",
        "courseCategory":"课程类别",
        "teacher":"课程老师",
        "teacher_id":"老师ID",
        "classId":"教学班ID",
        "classVolume":"教学班容量",
        "classPeople":"教学班已选人数",
        "courseRoom":"上课地点",
        "courseId":"课程号",
        "doId":"执行ID",
        "courseTime":"上课时间",
        "credit":"课程学分",
        "chooseSelf":"是否自选",
        "waiting":"是否待筛选"
        }]
}
```

## 板块课列表

```json
{
    "courseNumber":"教学班数量",
    "items":[{
        "courseTitle":"课程名程",
        "teacher":"课程老师",
        "teacher_id":"老师ID",
        "classId":"教学班ID",
        "doId":"执行ID",
        "kklxdm":"板块课1/2的特有ID",
        "classVolume":"教学班容量",
        "classPeople":"教学班已选人数",
        "courseRoom":"上课地点",
        "courseId":"课程号",
        "courseTime":"上课时间",
        "credit":"课程学分"
        }]
}
```