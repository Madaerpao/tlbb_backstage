# -*- coding: UTF-8 -*-
from flask import Flask,render_template,request
from performance import *
import myconf
#网页内容
my_website = myconf.config['my_website']

app = Flask(__name__)
#功能前台页面
@app.route('/')
def index():
    return render_template('index.html',my_website=my_website)
@app.route('/register')
def register():
    get_code = Id_code().x
    return render_template('register.html',get_code=get_code,my_website=my_website)
@app.route('/mpwd')
def mpwd():
    get_code = Id_code().x
    return render_template('mpwd.html',get_code=get_code,my_website=my_website)
@app.route('/mapsave')
def map_save():
    get_code = Id_code().x
    return render_template('mapsave.html',get_code=get_code,my_website=my_website)
@app.route('/unblock')
def account_unblock():
    get_code = Id_code().x
    return render_template('unblock.html',get_code=get_code,my_website=my_website)
@app.route('/gmpoint')
def gmpoint():
    get_code = Id_code().x
    return render_template('gmpoint.html', get_code=get_code, my_website=my_website)

#功能实现函数
@app.route('/register_result',methods=['POST','GET'])
def register_result():
    if request.method=='POST':
        result = request.form
        print(result)
        bg = Backstage()
        if result['password'] != result['re_password']:
            return '两次输入的密码不一致'
        usr = result['usr']
        passwd = result['password']
        q = result['superpwd']
        or_code = result['or_code']
        code_catch = result['usr_input']
        if or_code != code_catch:
            return '验证码错误！！！！！'
        response = bg.register(usr,passwd,q)
        return render_template('result.html', result=result, response=response)
    else:
        return render_template('result.html', response='注册需要输入账号、密码等信息！！！')
@app.route('/mpwd_result',methods=["POST",'GET'])
def mpwd_result():
    if request.method == 'POST':
        result = request.form
        or_code = result['or_code']
        code_catch = result['usr_input']
        if or_code != code_catch:
            return '验证码错误！！！！！'
        if result['password'] != result['re_password']:
            response = '两次输入的新密码不一致！！！！！'
            return render_template('result.html', response=response)
        usr = result['usr']
        question_demo = result['superpwd']
        new_passwd= result['password']
        bg = Backstage()
        response = bg.modify_passwd(usr=usr,question_demo=question_demo,new_passwd=new_passwd)
        return render_template('result.html',response=response)
    else:
        return '请求方式错误，请确保您输入了信息'
@app.route('/mapsave_result',methods=['POST','GET'])
def mapsave_result():
    if request.method == 'POST':
        result = request.form
        or_code = result['or_code']
        code_catch = result['usr_input']
        if result['password'] != result['re_password']:
            return '两次输入的密码不一致'
        if or_code != code_catch:
            return '验证码错误！！！！！'
        usr = result['usr']
        password = result['password']
        bg =Backstage()
        response = bg.char_save(usr=usr,passwd=password)
        return render_template('result.html',response=response)
    else:
        return '请求方式错误，请确保您输入了信息'
@app.route('/unblock_result',methods=["POST","GET"])
def unblock_result():
    if request.method == 'POST':
        result = request.form
        or_code = result['or_code']
        code_catch = result['usr_input']
        if result['password'] != result['re_password']:
            return '两次输入的密码不一致'
        if or_code != code_catch:
            return '验证码错误！！！！！'
        usr = result['usr']
        password = result['password']
        bg = Backstage()
        response = bg.block_over(usr=usr,password=password)
        return render_template('result.html', response=response)
    else:
        return '请求方式错误，请确保您输入了信息'
@app.route('/gmpoint_result',methods=["POST","GET"])
def gmpoint_result():
    if request.method == 'POST':
        result = request.form
        or_code = result['or_code']
        code_catch = result['usr_input']
        if or_code != code_catch:
            return '验证码错误！！！！！'
        password = result['password']
        conf_passwd = myconf.config['gm_tool_pwd']
        if password != conf_passwd:
            return 'Gm识别码错误！！！！非GM无法适用本功能！！！'
        usr = result['usr']
        point = result['gmpoints']
        bg = Backstage()
        response = bg.gm_point(usr,point)
        return render_template('result.html', response=response)
    else:
        return '请求方式错误，请确保您输入了信息'
if __name__ == '__main__':
    app.run()
