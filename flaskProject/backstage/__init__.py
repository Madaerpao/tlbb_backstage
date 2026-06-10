# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, session, redirect, url_for
from functools import wraps
from performance import *
import myconf
import os

# 网页内容
my_website = myconf.config.get('my_website', '#')

app = Flask(__name__)
# 配置随机的 Secret Key 以启用安全的 Session 机制
app.secret_key = os.urandom(24)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('admin_login_page'))
        return f(*args, **kwargs)
    return decorated_function

# 功能前台页面
@app.route('/')
def index():
    return render_template('index.html', my_website=my_website)

@app.route('/register')
def register():
    get_code = Id_code().x
    session['captcha'] = get_code
    return render_template('register.html', get_code=get_code, my_website=my_website)

@app.route('/mpwd')
def mpwd():
    get_code = Id_code().x
    session['captcha'] = get_code
    return render_template('mpwd.html', get_code=get_code, my_website=my_website)

@app.route('/mapsave')
def map_save():
    get_code = Id_code().x
    session['captcha'] = get_code
    return render_template('mapsave.html', get_code=get_code, my_website=my_website)

@app.route('/unblock')
def account_unblock():
    get_code = Id_code().x
    session['captcha'] = get_code
    return render_template('unblock.html', get_code=get_code, my_website=my_website)

@app.route('/gmpoint')
@admin_required
def gmpoint():
    get_code = Id_code().x
    session['captcha'] = get_code
    return render_template('gmpoint.html', get_code=get_code, my_website=my_website)

@app.route('/potential')
def potential():
    get_code = Id_code().x
    session['captcha'] = get_code
    return render_template('potential.html', get_code=get_code, my_website=my_website)

# 验证码通用检查
def check_captcha(form_data):
    code_catch = form_data.get('usr_input', '')
    if 'captcha' not in session or session['captcha'].lower() != code_catch.lower():
        return False
    return True

# 功能实现函数
@app.route('/register_result', methods=['POST', 'GET'])
def register_result():
    if request.method == 'POST':
        result = request.form
        if not check_captcha(result):
            return render_template('result.html', response='验证码错误！！！！！')
        
        if result.get('password') != result.get('re_password'):
            return render_template('result.html', response='两次输入的密码不一致')
            
        usr = result.get('usr')
        passwd = result.get('password')
        q = result.get('superpwd')
        
        bg = Backstage()
        response = bg.register(usr, passwd, q)
        return render_template('result.html', result=result, response=response)
    else:
        return render_template('result.html', response='请求方式错误，请确保您输入了信息')

@app.route('/mpwd_result', methods=["POST", 'GET'])
def mpwd_result():
    if request.method == 'POST':
        result = request.form
        if not check_captcha(result):
            return render_template('result.html', response='验证码错误！！！！！')
            
        if result.get('password') != result.get('re_password'):
            return render_template('result.html', response='两次输入的新密码不一致！！！！！')
            
        usr = result.get('usr')
        question_demo = result.get('superpwd')
        new_passwd = result.get('password')
        
        bg = Backstage()
        response = bg.modify_passwd(usr=usr, question_demo=question_demo, new_passwd=new_passwd)
        return render_template('result.html', response=response)
    else:
        return render_template('result.html', response='请求方式错误，请确保您输入了信息')

@app.route('/mapsave_result', methods=['POST', 'GET'])
def mapsave_result():
    if request.method == 'POST':
        result = request.form
        if not check_captcha(result):
            return render_template('result.html', response='验证码错误！！！！！')
            
        if result.get('password') != result.get('re_password'):
            return render_template('result.html', response='两次输入的密码不一致')
            
        usr = result.get('usr')
        password = result.get('password')
        
        bg = Backstage()
        response = bg.char_save(usr=usr, passwd=password)
        return render_template('result.html', response=response)
    else:
        return render_template('result.html', response='请求方式错误，请确保您输入了信息')

@app.route('/unblock_result', methods=["POST", "GET"])
def unblock_result():
    if request.method == 'POST':
        result = request.form
        if not check_captcha(result):
            return render_template('result.html', response='验证码错误！！！！！')
            
        if result.get('password') != result.get('re_password'):
            return render_template('result.html', response='两次输入的密码不一致')
            
        usr = result.get('usr')
        password = result.get('password')
        
        bg = Backstage()
        response = bg.block_over(usr=usr, password=password)
        return render_template('result.html', response=response)
    else:
        return render_template('result.html', response='请求方式错误，请确保您输入了信息')

@app.route('/gmpoint_result', methods=["POST", "GET"])
@admin_required
def gmpoint_result():
    if request.method == 'POST':
        result = request.form
        if not check_captcha(result):
            return render_template('result.html', response='验证码错误！！！！！')
            
        usr = result.get('usr')
        point = result.get('gmpoints')
        
        bg = Backstage()
        response = bg.gm_point(usr, point)
        return render_template('result.html', response=response)
    else:
        return render_template('result.html', response='请求方式错误，请确保您输入了信息')

@app.route('/potential_result', methods=["POST", "GET"])
def potential_result():
    if request.method == 'POST':
        result = request.form
        if not check_captcha(result):
            return render_template('result.html', response='验证码错误！！！！！')
            
        if result.get('password') != result.get('re_password'):
            return render_template('result.html', response='两次输入的密码不一致')
            
        usr = result.get('usr')
        password = result.get('password')
        points = result.get('points')
        
        bg = Backstage()
        response = bg.allocate_potential(usr, password, points)
        return render_template('result.html', response=response)
    else:
        return render_template('result.html', response='请求方式错误，请确保您输入了信息')

@app.route('/gmtools')
@admin_required
def gmtools():
    get_code = Id_code().x
    session['captcha'] = get_code
    return render_template('gmtools.html', get_code=get_code, my_website=my_website)

@app.route('/gmtools_result', methods=["POST", "GET"])
@admin_required
def gmtools_result():
    if request.method == 'POST':
        result = request.form
        if not check_captcha(result):
            return render_template('result.html', response='验证码错误！！！！！')
            
        event = result.get('event')
        eventnote = result.get('eventnote')
        param1 = result.get('param1', '')
        param2 = result.get('param2', '')
        param3 = result.get('param3', '')
        param4 = result.get('param4', '')
        
        bg = Backstage()
        response = bg.add_gm_event(event, eventnote, param1, param2, param3, param4)
        return render_template('result.html', response=response)
    else:
        return render_template('result.html', response='请求方式错误，请确保您输入了信息')

@app.route('/api/get_event', methods=['GET'])
def get_event():
    private_key = request.args.get('privateKey', '')
    bg = Backstage()
    response_str = bg.fetch_last_event(private_key)
    
    # 强制以 GBK 编码输出，并指定 header，防止天龙服务端 Lua 脚本接收到 UTF-8 导致游戏内中文乱码
    from flask import Response
    return Response(response_str.encode('gbk', errors='ignore'), content_type='text/plain; charset=gbk')

@app.route('/admin', methods=['GET'])
def admin_login_page():
    if session.get('is_admin'):
        return redirect(url_for('admin_dashboard'))
    get_code = Id_code().x
    session['captcha'] = get_code
    return render_template('admin_login.html', get_code=get_code, my_website=my_website)

@app.route('/admin_login', methods=['POST'])
def admin_login():
    result = request.form
    if not check_captcha(result):
        return render_template('result.html', response='验证码错误！！！！！')
        
    password = result.get('password')
    conf_passwd = myconf.config.get('gm_tool_pwd', '')
    if password != conf_passwd:
        return render_template('result.html', response='管理员密码错误！')
        
    session['is_admin'] = True
    return redirect(url_for('admin_dashboard'))

@app.route('/admin_logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))

@app.route('/admin_dashboard')
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html', my_website=my_website)

if __name__ == '__main__':
    app.run()
