from flask import Flask, session, render_template, request, jsonify
import hashlib, random, functools
import logging

import database as db
from topic_modeling import conclude_topic

''' 
报错信息:
    200: 成功访问页面
    403: 服务器拒绝请求
    500: 服务器内部错误
'''

# 创建flask实例对象
app = Flask(__name__)
app.config.from_object(db.DevelopmentConfig) # 配置app

print('secret_key: ', app.secret_key)
if __name__ == '__main__':
    with app.app_context(): # 在上下文环境中初始化数据库
        db_app = db.init_app(app)

# 设置日志级别
app.logger.setLevel(logging.INFO)


# 判断当前用户是否在session中。由于flask要求命名空间映射唯一，所以使用functools模块动态生成装饰器函数
def if_session(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_name' in session:
            return func(*args, **kwargs)
        else:
            print("user not in session, redirecting to login")
            return render_template("login_register.html")
    return wrapper

def create_session(id:int, name:str, email:str):
    session['user_email'] = email
    session['user_name'] = name
    session['user_id'] = id


# 创建根路由
@app.route('/')
def root():
    return index()


@app.route('/index', methods=["GET", "POST"])
@if_session
def index():
    if request.method == "GET":
        return render_template('index.html', userData={
            'user_email': session['user_email'],
            'user_name': session['user_name'],
        })

    elif request.method == "POST":
        page_sign = request.json['page_sign']
        private_data = request.json['private_data']
        print('user:',session['user_email'],'in:',page_sign, private_data)

        if page_sign == 'details':
            # 添加历史记录
            if (res := db.add_history(db_app, user_id=session['user_id'], doc_id=private_data))[0] != 200:
                return jsonify({'state': res[0], 'res': res[1]})
            # 查找文献
            res = db.search_literature(doc_id=private_data)[0]

            # 创建文献信息字典
            res_dict = {}
            for i in db.RSoE_title_dict:
                ti = eval(f'res.{i}')
                res_dict[i] = ti if ti != '' else '（没有记录）'
                if i == 'PD' and ti == '':
                    res_dict['PD'] = ''
            res_dict['id'] = private_data
            res_dict['Topic'] = conclude_topic(res_dict, model = 'LDA')

            # details likes {'TI':'xx', 'AU':'xx', ...}
            return  jsonify({'state': 200, 'privateHTML': render_template('details.html', details=jsonify(res_dict))})
        elif page_sign in ["home", "history", "developers", "document"]:
            return jsonify({'state': 200, 'privateHTML': render_template(f'{page_sign}.html')})
        else:
            return jsonify({'state': 404})


@app.route('/search', methods=["POST"])
@if_session
def search():
    search_key = request.json
    if search_key:
        print('user:',session['user_email'],'search: ', search_key)
        res = db.search_literature(author=search_key, title=search_key)
    else:
        print('user:',session['user_email'],'random search')
        # 随机查询5篇文献
        res = []
        for i in range(5):
            random_id = random.randint(1, db.RSoE_num)
            res += db.search_literature(doc_id=random_id)

    # 创建简要信息表
    ls = []
    for e in res:
        res_dict = {}
        for i in ['id', 'AU', 'TI', 'PD', 'PY']:
            res_dict[i] = eval(f'e.{i}')
        ls.append(res_dict.copy())
    return jsonify({'state': 200, 'data': ls})


@app.route('/history', methods=['GET'])
@if_session
def history():
    his = db.query_history(user_id=session['user_id'])
    historyData = []
    for i in range(1, 21):
        if (s := eval(f'his.h{i}')) != '':
            historyData.append(eval(s)) # s likes: '[doc_id, time]'
    # historyData likes [[doc_id, time, doc_title], [xx,xx,xxx], ...]
    return historyData


@app.route('/login_register', methods=["GET", "POST"])
def login_register():
    if request.method == 'GET':
        return render_template('login_register.html')
    elif request.method == 'POST':
        data = request.json
        data['password'] = hashlib.sha256(data['password'].encode()).hexdigest()
        if 'username' in data: # 为注册请求
            if data['username'] == '' or data['email'] == '' or data['password'] == '':
                return jsonify({'state': 403, "message": '注册用户名、邮箱、密码不能为空'})
            # with app.app_context():
            res = db.create_user(db_app, data['username'], data['email'], data['password'])  # 在数据库中创建用户
            if res[0] == 200:
                print('用户注册：', res[2].email)
                # 创建session对象存储用户名，将用户名存储到 session 中
                create_session(id = res[2].id, name=res[2].name, email = res[2].email)
                return jsonify({'state': 200, "message": res[1]})
            else: return jsonify({'state': res[0], "message": res[1]})

        else: # 为登入请求
            if data['email'] == '' or data['password'] == '':
                return jsonify({'state': 403, "message": '登入邮箱、密码不能为空'})
            # with app.app_context():
            res = db.query_user(email = data['email'])  # 在数据库中查找用户并核对密码
            if res[0]:
                if res[1].password == data['password']:
                    print('用户登入：', res[1].email)
                    create_session(id = res[1].id, name=res[1].name, email = res[1].email)
                    return jsonify({'state': 200, "message": "登入成功"})
                else:
                    return jsonify({'state': 403, 'message': '用户名或密码错误'})
            else:
                return jsonify({'state': 403, 'message':'用户不存在'})

@app.route('/logout')
def logout():
    session.clear()
    return render_template('login_register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


