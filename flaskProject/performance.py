# -*- coding: UTF-8 -*-

import hashlib
import myconf
import pymysql
import random

#验证码生成\检测

class Id_code(object):
    def __init__(self):
        y = 'abcdefghijklmnopqrstuvwxyz' + 'abcdefghijklmnopqrstuvwxyz'.upper()
        m = [str(random.randint(0, 9)), random.choice(y), random.choice(y), str(random.randint(0, 9))]
        w = ''
        for i in range(0, 5):
            n = random.choice(m)
            w += n
        self.x = w



#功能是否开启检测
def check_on(func):
    x = func.__name__
    def inner(*args,**kwargs):
        Tag = myconf.config.get(x, True)
        if Tag == False:
            return '功能未开启！！！请联系管理员'
        else:
            res = func(*args, **kwargs)
            return res
    return inner


class Backstage:
    @check_on
    def register(self, usr, passwd,q):
        conn = None
        try:
            conn = pymysql.connect(user='root', password=myconf.config['DB_PASSWORD'], host=myconf.config['IP'], database='web', port=myconf.config['DB_PORT'])
            with conn.cursor() as c:
                usr_full = usr + '@game.sohu.com'
                c.execute("select 1 from account where name=%s limit 1", (usr_full,))
                if c.fetchone():
                    return '注册失败，已经有相同账号存在！！！'
                
                pw = hashlib.md5(passwd.encode('utf-8')).hexdigest()
                if len(q) < 8:
                    return '注册失败，你输入的超级密码，必须大于等于8位数！！'
                
                question = hashlib.md5(q.encode('utf-8')).hexdigest()
                e = "1234@qq.com"
                
                sql_create = '''
                insert into account(name,password,question,email)
                VALUES (%s,%s,%s,%s)
                '''
                c.execute(sql_create, (usr_full, pw, question, e))
            conn.commit()
            return '注册成功！！！您的账号：%s\n您的密码：%s\n您的超级密码：%s' % (usr_full, passwd, q)
        except Exception as e:
            if conn:
                conn.rollback()
            return '注册失败\n' + str(e) + '\n请重启此程序重新注册，注意：您的账号和密码必须由数字和英文字母组成！！！！'
        finally:
            if conn:
                conn.close()

    @check_on
    def modify_passwd(self, usr, question_demo, new_passwd):
        conn = None
        try:
            conn = pymysql.connect(user='root', password=myconf.config['DB_PASSWORD'], host=myconf.config['IP'], database='web',port=myconf.config['DB_PORT'])
            with conn.cursor() as c:
                usr_full = usr + '@game.sohu.com'
                c.execute("select question from account where name=%s", (usr_full,))
                row = c.fetchone()
                if not row:
                    return '账号不存在！！！！请确定您是否填入了正确的账号！！！'
                
                qs = row[0]
                question = hashlib.md5(question_demo.encode('utf-8')).hexdigest()
                if question != qs:
                    return '超级密码错误！！！请重新输入！！！！'
                if len(new_passwd) == 0:
                    return '密码不能为空，请重新输入'
                
                md5_passwd = hashlib.md5(new_passwd.encode('utf-8')).hexdigest()
                sql_usr = "update account set password=%s where name=%s"
                c.execute(sql_usr, (md5_passwd, usr_full))
            conn.commit()
            return '您%s的账号已经将密码修改为%s，请牢记您的密码！！！！！' % (usr_full, new_passwd)
        except Exception as e:
            if conn:
                conn.rollback()
            return "修改失败！！！" + str(e)
        finally:
            if conn:
                conn.close()

    def char_save(self, usr, passwd):
        conn_tlbbdb = None
        conn_web = None
        try:
            conn_tlbbdb = pymysql.connect(user='root', password=myconf.config['DB_PASSWORD'], host=myconf.config['IP'], database='tlbbdb',port=myconf.config['DB_PORT'])
            conn_web = pymysql.connect(user='root', password=myconf.config['DB_PASSWORD'], host=myconf.config['IP'], database='web',port=myconf.config['DB_PORT'])
            
            with conn_web.cursor() as c_web:
                usr_full = usr + '@game.sohu.com'
                c_web.execute("select password from account where name=%s", (usr_full,))
                row = c_web.fetchone()
                if not row:
                    return '账号不存在！！！！请确定您是否填入了正确的账号！！！'
                
                server_pwd = row[0]
                real_pwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
                if real_pwd != server_pwd:
                    return '密码输入错误！！！请重新确认！！！！'
            
            with conn_tlbbdb.cursor() as c_tlbbdb:
                sql_find = "update t_char set scene=2,xpos=16000,zpos=17000 where accname=%s;"
                c_tlbbdb.execute(sql_find, (usr_full,))
            
            conn_tlbbdb.commit()
            conn_web.commit()
            return '自救成功！！！！赶快上线看看吧！！！'
        except Exception as e:
            if conn_web:
                conn_web.rollback()
            if conn_tlbbdb:
                conn_tlbbdb.rollback()
            return '地图自救失败！！！' + str(e)
        finally:
            if conn_web:
                conn_web.close()
            if conn_tlbbdb:
                conn_tlbbdb.close()

    def block_over(self, usr, password):
        conn_tlbbdb = None
        conn_web = None
        try:
            conn_tlbbdb = pymysql.connect(user='root', password=myconf.config['DB_PASSWORD'], host=myconf.config['IP'], database='tlbbdb',port=myconf.config['DB_PORT'])
            conn_web = pymysql.connect(user='root', password=myconf.config['DB_PASSWORD'], host=myconf.config['IP'], database='web',port=myconf.config['DB_PORT'])
            
            usr_full = usr + '@game.sohu.com'
            with conn_web.cursor() as c_web:
                c_web.execute("select password from account where name=%s", (usr_full,))
                row = c_web.fetchone()
                if not row:
                    return '账号不存在！！！！请确定您是否填入了正确的账号！！！'
                
                server_pwd = row[0]
                real_pwd = hashlib.md5(password.encode('utf-8')).hexdigest()
                if real_pwd != server_pwd:
                    return '密码输入错误！！！请重新确认！！！！'
                
                sql_web = "update account set is_lock=0,id_card=null where name=%s"
                c_web.execute(sql_web, (usr_full,))
            
            with conn_tlbbdb.cursor() as c_tlbbdb:
                sql_tlbbdb = "update t_char set isvalid=1,settings='0080F5200000040000000173010000017D010000018101000000000000000000000000000000000001160000000123000000020100000001010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000FF0000000000000000000000000000D233000000000000000000000000000128B3420E0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' where accname=%s"
                c_tlbbdb.execute(sql_tlbbdb, (usr_full,))
            
            conn_web.commit()
            conn_tlbbdb.commit()
            return '解封成功！！！！快去登录游戏试试吧！！！！'
        except Exception as e:
            if conn_web:
                conn_web.rollback()
            if conn_tlbbdb:
                conn_tlbbdb.rollback()
            return '解封失败: ' + str(e)
        finally:
            if conn_web:
                conn_web.close()
            if conn_tlbbdb:
                conn_tlbbdb.close()

    @check_on
    def gm_point(self,usr,points):
        conn_web = None
        try:
            conn_web = pymysql.connect(user='root', password=myconf.config['DB_PASSWORD'], host=myconf.config['IP'], database='web', port=myconf.config['DB_PORT'])
            with conn_web.cursor() as c_web:
                usr_full = usr + '@game.sohu.com'
                c_web.execute("select 1 from account where name=%s limit 1", (usr_full,))
                if not c_web.fetchone():
                    return '账号不存在！！！！请确定您是否填入了正确的账号！！！'
                
                try:
                    points = int(points)
                except ValueError:
                    return '输入的数值不是整数，请再次确认！！！'
                
                sql_web = "update account set point=point+%s where name=%s"
                c_web.execute(sql_web, (points, usr_full))
            conn_web.commit()
            return '充值成功！！！！快去登录游戏试试吧！！！！'
        except Exception as e:
            if conn_web:
                conn_web.rollback()
            return '充值失败: ' + str(e)
        finally:
            if conn_web:
                conn_web.close()

    @check_on
    def allocate_potential(self, usr, password, points):
        conn_tlbbdb = None
        conn_web = None
        try:
            conn_tlbbdb = pymysql.connect(user='root', password=myconf.config['DB_PASSWORD'], host=myconf.config['IP'], database='tlbbdb',port=myconf.config['DB_PORT'])
            conn_web = pymysql.connect(user='root', password=myconf.config['DB_PASSWORD'], host=myconf.config['IP'], database='web',port=myconf.config['DB_PORT'])
            
            usr_full = usr + '@game.sohu.com'
            with conn_web.cursor() as c_web:
                c_web.execute("select password from account where name=%s", (usr_full,))
                row = c_web.fetchone()
                if not row:
                    return '账号不存在！！！！请确定您是否填入了正确的账号！！！'
                
                server_pwd = row[0]
                real_pwd = hashlib.md5(password.encode('utf-8')).hexdigest()
                if real_pwd != server_pwd:
                    return '密码输入错误！！！请重新确认！！！！'
                    
            with conn_tlbbdb.cursor() as c_tlbbdb:
                try:
                    points = int(points)
                except ValueError:
                    return '潜能点数必须为整数！！！'
                
                if points <= 0 or points > 1000000:
                    return '潜能点数不合法（需在 1 到 1000000 之间）！！！'
                    
                sql_tlbbdb = "update t_char set remainpoints = remainpoints + %s where accname=%s"
                c_tlbbdb.execute(sql_tlbbdb, (points, usr_full))
                
            conn_web.commit()
            conn_tlbbdb.commit()
            return '潜能点分配成功！！！！快去登录游戏看看吧！！！！'
            
        except Exception as e:
            if conn_web:
                conn_web.rollback()
            if conn_tlbbdb:
                conn_tlbbdb.rollback()
            return '潜能分配失败: ' + str(e)
        finally:
            if conn_web:
                conn_web.close()
            if conn_tlbbdb:
                conn_tlbbdb.close()

    @check_on
    def add_gm_event(self, event, eventnote, param1, param2, param3, param4):
        conn_web = None
        try:
            conn_web = pymysql.connect(user='root', password=myconf.config['DB_PASSWORD'], host=myconf.config['IP'], database='web', port=myconf.config['DB_PORT'])
            with conn_web.cursor() as c_web:
                c_web.execute("SHOW TABLES LIKE 'eventlist'")
                if not c_web.fetchone():
                    sql_create = '''
                    CREATE TABLE `eventlist` (
                      `id` int(11) NOT NULL AUTO_INCREMENT,
                      `event` varchar(255) NOT NULL COMMENT '事件标识',
                      `eventnote` varchar(255) NOT NULL COMMENT '事件说明',
                      `createtime` int(11) NOT NULL COMMENT '事件创建时间',
                      `status` tinyint(2) unsigned NOT NULL DEFAULT '0' COMMENT '执行状态',
                      `requesttime` int(11) unsigned DEFAULT '0' COMMENT '事件请求回执时间',
                      `param1` varchar(255) DEFAULT NULL COMMENT '参数1',
                      `param2` varchar(255) DEFAULT NULL COMMENT '参数2',
                      `param3` varchar(255) DEFAULT NULL COMMENT '参数3',
                      `param4` varchar(255) DEFAULT NULL COMMENT '参数4',
                      PRIMARY KEY (`id`)
                    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=gbk;
                    '''
                    c_web.execute(sql_create)
                
                import time
                create_time = int(time.time())
                
                sql_insert = """
                INSERT INTO eventlist (event, eventnote, createtime, status, param1, param2, param3, param4)
                VALUES (%s, %s, %s, 0, %s, %s, %s, %s)
                """
                c_web.execute(sql_insert, (event, eventnote, create_time, param1, param2, param3, param4))
                
            conn_web.commit()
            return '事件发送成功！'
        except Exception as e:
            if conn_web:
                conn_web.rollback()
            return '事件发送失败: ' + str(e)
        finally:
            if conn_web:
                conn_web.close()

    def fetch_last_event(self, privateKey):
        if privateKey != myconf.config.get('private_key', ''):
            return ''
            
        conn_web = None
        try:
            conn_web = pymysql.connect(user='root', password=myconf.config['DB_PASSWORD'], host=myconf.config['IP'], database='web', port=myconf.config['DB_PORT'])
            with conn_web.cursor(pymysql.cursors.DictCursor) as c_web:
                c_web.execute("SHOW TABLES LIKE 'eventlist'")
                if not c_web.fetchone():
                    return ''
                    
                sql_fetch = "SELECT * FROM eventlist WHERE status = 0 ORDER BY id DESC LIMIT 1"
                c_web.execute(sql_fetch)
                res = c_web.fetchone()
                
                if res:
                    import time
                    request_time = int(time.time())
                    sql_update = "UPDATE eventlist SET status = 1, requesttime = %s WHERE id = %s"
                    c_web.execute(sql_update, (request_time, res['id']))
                    conn_web.commit()
                    
                    p1 = res.get('param1') or ''
                    p2 = res.get('param2') or ''
                    p3 = res.get('param3') or ''
                    p4 = res.get('param4') or ''
                    return f"{res['id']},{res['event']},{p1},{p2},{p3},{p4}"
                else:
                    return ''
        except Exception as e:
            if conn_web:
                conn_web.rollback()
            return ''
        finally:
            if conn_web:
                conn_web.close()
