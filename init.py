if __name__ == '__main__':
    import json
    # 将数据库配置写入本地，方便下次启动
    data = {"login_name": input('请输入数据库用户名：'), "password": input('请输入密码：'),
            "host": "127.0.0.1:3306",
            "database_name": "literaturesearch"}

    with open ('./db_setting.json', 'w') as f:
        json.dump(data, f)


    import app as flask_app
    with flask_app.app.app_context():  # 在上下文环境中初始化数据库
        db_app = flask_app.db.init_app(flask_app.app, first_write=True)


    import topic_modeling
    print('开始下载NTLK数据')
    topic_modeling.nltk.download('averaged_perceptron_tagger')
    print('初始化完成，可以启动Flask！')