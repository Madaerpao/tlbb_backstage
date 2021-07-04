# -*- coding: UTF-8 -*-

import hashlib

import pymysql


class Backstage:
    def register(self, usr, passwd, q):
        conn = pymysql.connect(user='root', password='修改为您的数据库密码', host='修改为您的Linux机IP地址', database='web')
        c = conn.cursor()
        sql_usr = '''
            select name from account
                '''
        c.execute(sql_usr)
        names = c.fetchall()
        name_list = []
        for name_tuple in names:
            name = name_tuple[0]
            name_list.append(name)
        usr = usr + '@game.sohu.com'
        if usr in name_list:
            return '注册失败，已经有相同账号存在！！！'
        else:
            usr = "'" + usr + "'"
            pw = "'" + hashlib.md5(passwd.encode('utf-8')).hexdigest() + "'"
            if len(q) < 8:
                return '注册失败，你输入的超级密码，必须大于等于8位数！！'
            else:
                question = "'" + hashlib.md5(q.encode('utf-8')).hexdigest() + "'"
                e = "'" + "1234@qq.com" + "'"
                try:
                    sql_create = '''
                    insert into account(name,password,question,email
                    )
                    VALUES (%s,%s,%s,%s)
                    ''' % (usr, pw, question, e)
                    c.execute(sql_create)
                    conn.commit()
                    c.close()
                    conn.close()
                    data = '注册成功！！！您的账号：%s' % usr + '\n' + '您的密码：%s' % passwd + '\n' + '您的超级密码：%s' % q
                    return data
                except Exception as e:
                    conn.rollback()
                    c.close()
                    conn.close()
                    data = '注册失败' + '\n' + e + '\n' + '请重启此程序重新注册，注意：您的账号和密码必须由数字和英文字母组成！！！！'
                    return data

    def modify_passwd(self, usr, question_demo, new_passwd):
        conn = pymysql.connect(user='root', password='修改为您的数据库密码', host='修改为您的Linux机IP地址', database='web')
        c = conn.cursor()
        sql_usr = '''
            select name from account
                '''
        c.execute(sql_usr)
        names = c.fetchall()
        name_list = []
        usr = usr + '@game.sohu.com'
        for name_tuple in names:
            name = name_tuple[0]
            name_list.append(name)
        if not usr in name_list:
            return '账号不存在！！！！请确定您是否填入了正确的账号！！！'
        sql_q = '''
        select question from account where name='%s'
        ''' % usr
        c.execute(sql_q)
        qs = c.fetchall()[0][0]
        question = hashlib.md5(question_demo.encode('utf-8')).hexdigest()
        if question != qs:
            return '超级密码错误！！！请重新输入！！！！'
        if len(new_passwd) == 0:
            return '密码不能为空，请重新输入'
        md5_passwd = hashlib.md5(new_passwd.encode('utf-8')).hexdigest()
        try:
            sql_usr = '''
                update account set password='%s' where name='%s'
                    ''' % (md5_passwd, usr)
            c.execute(sql_usr)
            conn.commit()
            c.close()
            conn.close()
            return '您%s的账号已经将密码修改为%s，请牢记您的密码！！！！！' % (usr, new_passwd)
        except Exception as e:
            conn.rollback()
            c.close()
            conn.close()
            data = "修改失败！！！" + e
            return data

    def char_save(self, usr, passwd):
        conn = pymysql.connect(user='root', password='修改为您的数据库密码', host='修改为您的Linux机IP地址', database='tlbbdb')
        c = conn.cursor()
        conn_web = pymysql.connect(user='root', password='修改为您的数据库密码', host='修改为您的Linux机IP地址', database='web')
        c_web = conn_web.cursor()
        sql_usr = '''
            select accname from t_char
                '''
        c.execute(sql_usr)
        names = c.fetchall()
        name_list = []
        usr = usr + '@game.sohu.com'
        for name_tuple in names:
            name = name_tuple[0]
            name_list.append(name)
        if not usr in name_list:
            return '账号不存在！！！！请确定您是否填入了正确的账号！！！'
        real_pwd = hashlib.md5(passwd.encode('utf-8')).hexdigest()
        pwd_sql = '''
            select password from account where name='%s'
            ''' % usr
        c_web.execute(pwd_sql)
        server_pwd = c_web.fetchall()[0][0]
        if real_pwd != server_pwd:
            return '密码输入错误！！！请重新确认！！！！'
        sql_find = '''
            update t_char set scene=2,xpos=16000,zpos=17000 where accname='%s';
        ''' % usr
        try:
            c.execute(sql_find)
            conn.commit()
            c.close()
            conn.close()
            c_web.close()
            conn_web.close()
            return '自救成功！！！！赶快上线看看吧！！！'
        except Exception as e:
            conn.rollback()
            c.close()
            conn.close()
            c_web.close()
            conn_web.close()
            data = '地图自救失败！！！' + e
            return data

    def block_over(self, usr, password):
        conn_tlbbdb = pymysql.connect(user='root', password='修改为您的数据库密码', host='修改为您的Linux机IP地址', database='tlbbdb')
        c_tlbbdb = conn_tlbbdb.cursor()
        conn_web = pymysql.connect(user='root', password='修改为您的数据库密码', host='修改为您的Linux机IP地址', database='web')
        c_web = conn_web.cursor()
        usr = usr + '@game.sohu.com'
        # 检测账号是否存在
        sql_usr = '''
                    select name from account
                        '''
        c_web.execute(sql_usr)
        names = c_web.fetchall()
        name_list = []
        for name_tuple in names:
            name = name_tuple[0]
            name_list.append(name)
        if not usr in name_list:
            return '账号不存在！！！！请确定您是否填入了正确的账号！！！'
        # 检测密码是否正确
        real_pwd = hashlib.md5(password.encode('utf-8')).hexdigest()
        pwd_sql = '''
                    select password from account where name='%s'
                    ''' % usr
        c_web.execute(pwd_sql)
        server_pwd = c_web.fetchall()[0][0]
        if real_pwd != server_pwd:
            return '密码输入错误！！！请重新确认！！！！'
        sql_web = '''
            update account set is_lock=0,id_card=null where name='%s'
        ''' % usr
        sql_tlbbdb = '''
            update t_char set isvalid=1,settings='0080F5200000040000000173010000017D01000001810100000000000000000000000000000000000116000000012300000002010000000101000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000000FF0000000000000000000000000000D233000000000000000000000000000128B3420E0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000' where accname='%s'
        ''' % usr
        try:
            c_web.execute(sql_web)
            conn_web.commit()
            c_tlbbdb.execute(sql_tlbbdb)
            conn_tlbbdb.commit()
            c_tlbbdb.close()
            c_web.close()
            conn_tlbbdb.close()
            conn_web.close()
            return '解封成功！！！！快去登录游戏试试吧！！！！'
        except Exception as e:
            data = '解封失败' + e
            conn_web.rollback()
            conn_tlbbdb.rollback()
            c_tlbbdb.close()
            c_web.close()
            conn_tlbbdb.close()
            conn_web.close()
            return data
# if __name__ == '__main__':
#     print('-----------------------------------------------')
#     print('1.输入 register ，则进入 注册账号 选项！！')
#     print('2.输入 modify_passwd ，则进入 修改账号密码 选项！！！！')
#     print('3.输入 char_save ，则进入 地图自救 选项！！！！')
#     print('4.输入 block_over ，则进入 自助解封 选项！！！！')
#     print('后续将有其他角色后台功能完善！！！！')
#     print('-----------------------------------------------')
#     usr_choose = input('请输入您的选项：')
#     backstage = Backstage()
#     while not hasattr(backstage,usr_choose):
#         print('没有此项功能，请重新输入！！！！')
#         usr_choose = input('请输入您的选项：')
#     else:
#         func = getattr(backstage, usr_choose)
#         func()
