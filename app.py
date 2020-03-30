from flask import Flask
from flask import request
from flask import  session
import mysql.connector

# 实例化一个Flask类，同时为app设置secret_key
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dasdefaf9*&*Tfdad'  # 该secret_key 为随机字符串

# 建立一个MYSQL连接：
conn = mysql.connector.connect(
    host='localhost', user='bbt', passwd='bbtbbtbbt', database='bbt_demo', charset='utf8mb4')
db = conn.cursor()

# 首先，我们先写一个注册接口！

@app.route('/bbt/users', methods=['POST'])
def register():
    # 在此我们使用了restful风格。可以看到甚至不需要告诉你这是一个什么接口，仅仅告诉你url以及method，就可以一目了然该接口是干什么的

    # 接着，我们考虑实现该功能需要哪些处理，很明显，首先我们要把前端发来的数据拿出来，这里我们需要引入request

    data = request.get_json()  # 在content-type= application/json时 ，可以通过该方法获取数据
    username = data['username']
    password = data['password']

# 接着，需要去判断注册用的用户名数据库里是否已存在该用户，前面我们已经建立了连接，在此时就派上用场了

    db.execute('select `username` from users where `username`= %s', (username,))
    result = db.fetchall()
    if result:
        return {
            'errcode': 400,
            'errmsg': '该用户名已被注册'
        }, 400

# 接着，只要查询不存在用户名，则可以插入数据，并且成功给前端
    db.execute(
        'insert into users (`username`,`password`)values (%s,%s)', (username, password))
    if db.rowcount > 0:  # rowcount 为影响数据数目，成功插入即影响一条数据，同理update,delete
        return{
            'errcode': 0,
            'errmsg': '注册成功'
        }, 200

    return {
            'errcode': 400,
            'errmsg': '出现错误~请重试'
        }, 400

@app.route('/bbt/login',methods=['POST'])
def login():
    data = request.get_json()
    username=data['username']
    password=data['password']

    db.execute('select `id` from users where `username`=%s and `password`=%s',(username,password))
    result = db.fetchone()

    if result:
        session['user_id']=result[0 ]
        return {
            'errcode ':0,
            'errmsg':'登录成功'
        },200
    return {
            'errcode':401,
            'errmsg':'用户不存在或密码错误'
        },401
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9990)  # 将运行在本地回路ip的9990端口
