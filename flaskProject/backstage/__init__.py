# -*- coding: UTF-8 -*-
from flask import Flask,render_template,request
from performance import Backstage
app = Flask(__name__)
#功能前台页面
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/mpwd')
def mpwd():
    return render_template('mpwd.html')
@app.route('/mapsave')
def map_save():
    return render_template('mapsave.html')
@app.route('/unblock')
def account_unblock():
    return render_template('unblock.html')



#功能实现函数
@app.route('/register_result',methods=['POST','GET'])
def register_result():
    if request.method=='POST':
        result = request.form
        bg = Backstage()
        usr = result['usr']
        passwd = result['password']
        q = result['superpwd']
        response = bg.register(usr,passwd,q)
        return render_template('result.html', result=result, response=response)
    else:
        return render_template('result.html', response='注册需要输入账号、密码等信息！！！')
@app.route('/mpwd_result',methods=["POST",'GET'])
def mpwd_result():
    if request.method == 'POST':
        result = request.form
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
        usr = result['usr']
        password = result['password']
        bg = Backstage()
        response = bg.block_over(usr=usr,password=password)
        return render_template('result.html', response=response)
    else:
        return '请求方式错误，请确保您输入了信息'
if __name__ == '__main__':
    app.run()
