# tlbb_backstage

**TL单Linux账号管理后台**

## 说明

**1.双机开服的朋友可以略过！！！！兄弟们可能会觉得没什么用！！！-_-||-_-||-_-||-_-||**

**2.我也是小白，考虑到有些单Linux机的朋友，自己想开群服单纯供朋友娱乐，却经常莫名封号、封角色，除了直接给出去GM工具，就没有别的办法能够实现自助注册、自助解封、地图自救、修改密码功能，所以用Python写了个小框架。有能力的也可以自己加功能，如分配潜能、背包清理之类的，只需要写一个简单的SQL的update语句即可。**

**3.我也有写一个单Linux可以隐去Ip和端口的登录器，功能已经能够实现了。只是没有好看界面，现在还在写图形界面，有需要的朋友可以来找我拿，或者一起开发！！！**

---

## 功能介绍

1.不依赖登录器的web轻量级应用，无论你是单Linux还是双机，都可使用。

2.支持在线注册、自助解封、地图自救、修改密码等功能。

3.源码可修改、变动，按照已经写好的performance.py文件的功能模板，可以自行增加新功能。

4.可以通过增加账号验证条件，将注册后台改为在线分配账号点数工具。

**效果展示：**  示例页面： http://www.zkwd888.ltd:8881/  


![輸入圖片說明](https://images.gitee.com/uploads/images/2021/0705/165313_6cb3c3c8_8680032.png "image-20210705164738062.png")

![輸入圖片說明](https://images.gitee.com/uploads/images/2021/0705/165411_719435e9_8680032.png "image-20210705164804720.png")

![輸入圖片說明](https://images.gitee.com/uploads/images/2021/0705/165421_e9f35497_8680032.png "image-20210705164824808.png")

![輸入圖片說明](https://images.gitee.com/uploads/images/2021/0705/165429_2293d0f3_8680032.png "image-20210705164940048.png")


---

## 使用方法

获取安装包：

如果在线获取的话 则需要如下命令

```shell
cd ~ && git clone https://gitee.com/zhao-kai135/tlbb_backstage.git .
```

如果是自己下载压缩包，上传服务器的，不需要执行以上命令

1.打开 flaskProject/myconf.py ，按照说明修改配置文件：

```python
config = {
    'IP':'您的数据库Ip',                   #数据库所在IP，一般是Linux的IP地址
    'DB_PASSWORD':'您的数据库密码',    #数据库密码，不是Linux密码
    'DB_PORT':3306,                 #数据库端口默认3306，如果您的不是3306，请自行更改
    'register': True,               #网页自助注册功能是否开启，默认开启，False关闭
    'modify_passwd':True,            #修改密码功能是否开启，默认开启，False关闭
    'gm_point':True,                #GM在线发放点数功能，默认开始，False关闭
    'gm_tool_pwd':'1TeStMySeRvErGmToOl.29',     #可自定，GM在线功能的密码，如果上面的功能未开启，可以不进行修改
    'my_website':'https://www.zkwd888.ltd' #自己有主页的话写自己的，没有的话就随意填写，可不修改

}

```


注意：

- .py文件里面的单引号要保留！！
- 数据库密码不是Linux密码，不要输错哦！！
- True/False控制功能是否开启
- 如果开启了Gm在线发放点数功能，请牢记您的Gm在线功能密码（单引号内部的就是您的GM密码），避免泄露！！！
- GM功能目前只能发放点数，在Gm管理界面输入GM密码、发放点数的账号、发放的数额。

2.将整个flaskProject上传至您的Linux的root目录下，然后输入命令：

**如果前面是在线获取安装包的，请执行以下命令：**

```shell
cd /root/tlbb_backstage/flaskProject

chmod -R 777 /root/tlbb_backstage/flaskProject

sh run.sh
```

> 注意：中途出现红色的**Warining 、DEPRECATION**之类的，不要慌，不是报错 ！！！

**如果前面是自行获取安装包上传至服务器的，请执行以下命令：**

```shell
cd /root/flaskProject

chmod -R 777 /root/flaskProject

sh run.sh
```

3.访问一下 `http://你的IP:8881` ，测试一下有没有运行起来吧！！！！如果有问题也可以一起探讨哦！！

---

## 新增功能计划....（未实现）

+ 增加验证码，避免页面被恶意频繁访问、恶意攻击MySQL数据库。==（已经初步实现）==

+ 优化前端HTML页面，提升页面美观度。

+ 支持潜能点数分配功能

+ 支持自助打孔功能

+ 支持背包、仓库清理功能等

+ .......

  产生Bug，或者是有其他需求，请issue提出，有能力的话我会修复、增加的