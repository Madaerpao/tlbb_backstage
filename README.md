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

---

## 使用方法

1.打开 flaskProject/performance.py ，在其中 搜索并替换 如下两端字符为指定内容（可以看图片哦）：

```
修改为您的数据库密码

修改为您的Linux机IP地址
```

![輸入圖片說明](https://images.gitee.com/uploads/images/2021/0704/223017_2f3934cf_8680032.png "替换文本1.png")

![輸入圖片說明](https://images.gitee.com/uploads/images/2021/0704/223033_baf2e94f_8680032.png "替换文本2.png")


注意：

- 要全部替换！！！！
- .py文件里面的单引号要保留！！
- 数据库密码不是Linux密码，不要输错哦！！


2.将整个flaskProject上传至您的Linux的root目录下，然后输入命令：

```shell
cd /root/flaskProject

chmod -R 777 /root/flaskProject

sh run.sh
```

> 注意：中途出现红色的**Warining 、DEPRECATION**之类的，不要慌，不是报错 ！！！

3.访问一下 `http://你的IP:8881` ，测试一下有没有运行起来吧！！！！如果有问题也可以一起探讨哦！！

---

## 新增功能计划....（未实现）

+ 增加验证码，避免页面被恶意频繁访问、恶意攻击MySQL数据库。

+ 优化前端HTML页面，提升页面美观度。

+ 支持潜能点数分配功能

+ 支持自助打孔功能

+ 支持背包、仓库清理功能等

+ .......

  其他需求，请issue提出，有能力的话我会加上的