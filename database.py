from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import os, datetime, json

class BaseConfig:
    SECRET_KEY = '66666666'
    # SECRET_KEY = os.urandom(24) # 每次重启服务器都更换session
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=7) # session每7天过期

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    with open ('./db_setting.json', 'r') as f:
        data = json.load(f)
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{data['login_name']}:{data['password']}@{data['host']}/{data['database_name']}?charset=utf8mb4"
    # 缓存配置
    CACHE_TYPE = "simple"
    # CACHE_TYPE = "RedisCache"
    # CACHE_REDIS_HOST = "127.0.0.1"
    # CACHE_REDIS_PORT = 6379


RSoE_title_dict = {
    "AB": "摘要",
    "TI": "文献标题",
    "AU": "作者",

    "PY": "出版年",
    "PD": "出版日期",

    "U1": "被引用次数（最近 180 天）",
    "U2": "被引用次数（2013 年至今）",
    "UT": "入藏号",
}
def init_app(app, first_write = False):
    db = SQLAlchemy(app)
    global User, RSoE, User_history, RSoE_num
    # 创建用户表单
    class User(db.Model):
        __tablename__ = 'user'  # 设置表名, 表名默认为类名小写
        id = db.Column(db.Integer, primary_key=True) # 设置主键, 默认自增
        name = db.Column(db.String(80), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False) # 设置字段名 和 唯一约束
        password = db.Column(db.String(120), nullable=False)
        create_time = db.Column(db.String(64))
        # 执行print(实例)时返回的内容
        def __repr__(self):
            return f'用户名：{self.name} id：{self.id} 邮箱：{self.email} 创建时间：{self.create_time}'

    # 创建用户历史记录表单
    class User_history(db.Model):
        __tablename__ = 'user_history'
        # 只存放20条数据，滚动更新
        user_id = db.Column(db.Integer, primary_key=True)
        h1 = db.Column(db.Text)
        h2 = db.Column(db.Text)
        h3 = db.Column(db.Text)
        h4 = db.Column(db.Text)
        h5 = db.Column(db.Text)
        h6 = db.Column(db.Text)
        h7 = db.Column(db.Text)
        h8 = db.Column(db.Text)
        h9 = db.Column(db.Text)
        h10 = db.Column(db.Text)
        h11 = db.Column(db.Text)
        h12 = db.Column(db.Text)
        h13 = db.Column(db.Text)
        h14 = db.Column(db.Text)
        h15 = db.Column(db.Text)
        h16 = db.Column(db.Text)
        h17 = db.Column(db.Text)
        h18 = db.Column(db.Text)
        h19 = db.Column(db.Text)
        h20 = db.Column(db.Text)

    # 创建Remote Sensing of Environment期刊数据表单
    class RSoE(db.Model):
        __tablename__ = 'remote_sensing_of_environment'
        # all_title_list = [
        #     "PT", "AU", "AF", "TI", "SO", "LA", "DT", "DE", "ID", "AB", "C1", "C3", "EM", "OI",
        #     "FU", "FX", "NR", "TC", "Z9", "U1", "U2", "PU", "PI", "PA", "SN", "EI", "J9", "JI",
        #     "PD", "PY", "VL", "AR", "DI", "PG", "WC", "WE", "SC", "GA", "UT", "OA", "DA", "ER"
        # ]

        # 创建属性名
        id = db.Column(db.Integer, primary_key=True)
        AB = db.Column(db.Text)
        TI = db.Column(db.Text)
        AU = db.Column(db.Text)
        PY = db.Column(db.Integer)
        PD = db.Column(db.Text)
        NR = db.Column(db.Integer)
        U1 = db.Column(db.Integer)
        U2 = db.Column(db.Integer)
        UT = db.Column(db.String(50))

    if first_write:
        db.drop_all() # 删除所有继承自db.Model的表，即上述类对应的表单
        print("清除数据库遗留信息")

    db.create_all()
    # 写入文献数据
    if first_write:
        print("写入文献数据中，...")
        path = "./RSoE OriginData"
        title_dict = {}
        for i in RSoE_title_dict:
            title_dict[i] = ''
        for file in os.listdir(path):
            with open(path + "/" + file, 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    if line != "\n":
                        # print(line[:-2])
                        ti = line[:2]
                        if ti in title_dict:
                            title = str(ti)
                            title_dict[title] = line[3:-1]
                            same_title = True
                        elif ti == '  ' and same_title:
                            title_dict[title] += line[2:-1]
                        else: # 行标题变了

                            same_title = False
                    else: # 为空行，写入前一条文献的数据
                        # print(title_dict)
                        db.session.add(RSoE(**title_dict))
                        db.session.commit()
                        # 清空前一条文献的数据
                        for i in RSoE_title_dict:
                            title_dict[i] = ''
        print("数据库初始化完成！")
    RSoE_num = RSoE.query.count()
    return db



history_title = {'h1': '', 'h2': '', 'h3': '', 'h4': '', 'h5': '', 'h6': '', 'h7': '', 'h8': '', 'h9': '', 'h10': '',
            'h11': '', 'h12': '', 'h13': '', 'h14': '', 'h15': '', 'h16': '', 'h17': '', 'h18': '', 'h19': '','h20': ''}
def create_user(db_app, username:str, email:str, password:str):
    try:
        # 创建用户
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        new_user = User(name=username, email=email, password=password, create_time=current_time)
        db_app.session.add(new_user)
        db_app.session.commit() # 提交更改

        # 创建空的用户历史记录
        user =  User.query.filter_by(email = email).first()
        user_his_init = User_history(user_id = user.id, **history_title)
        db_app.session.add(user_his_init)
        db_app.session.commit()
    except IntegrityError:
        db_app.session.rollback()
        return 403, "创建用户失败，此邮箱已被注册"
    except SQLAlchemyError as e:
        db_app.session.rollback()
        return 500, f"注册失败，数据库错误: {str(e)}"
    except Exception as e:
        db_app.session.rollback()
        return 500, f"注册失败，未知错误: {str(e)}"
    else:
        return 200, "创建用户成功！", user

def query_user(email:str = None, id:int = None):
    if id:
        if user := User.query.filter_by(id = id).first():
            return True, user
        else: return False, '用户不存在'
    if email:
        if user := User.query.filter_by(email = email).first():
            return True, user
        else: return False, '用户不存在'


def search_literature(doc_id:int = None, author = None, title = None):
    res = []
    if doc_id:
        res += [RSoE.query.get(doc_id)]
    if author:
        res += RSoE.query.filter(RSoE.AU.ilike(f'%{author}%')).all()
    if title:
        res += RSoE.query.filter(RSoE.TI.ilike(f'%{title}%')).all()
    return res

def query_history(user_id):
    his = User_history.query.get(user_id)
    return his

def add_history(db_app, user_id, doc_id):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_his=f"[{doc_id}, '{current_time}', '{search_literature(doc_id=doc_id)[0].TI}']"
    # 更新用户历史记录
    user_history = query_history(user_id=user_id)

    try:
        for i in range(20, 1, -1):
            exec(f'user_history.h{i} = user_history.h{i-1}')
            db_app.session.commit()
        user_history.h1 = new_his
        db_app.session.commit()
    except SQLAlchemyError as e:
        return 500, f"写入失败，数据库错误: {str(e)}"
    except Exception as e:
        return 500, f"写入失败，未知错误: {str(e)}"
    else:
        return 200, "成功写入历史记录"

