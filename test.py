import pymysql
import datetime
import uuid
from flask import Flask
from flask import request
import json
db = pymysql.connect(host = "jp.pkmgtdz.xyz" , port = 3306 , user = "ljx" , password = "lijixuan" , database = "UserSignIn")
cursor = db.cursor()

# x = uuid.uuid1()
# print(x.get_node())

def register(username):
    key = uuid.uuid1()
    sql = "insert into user(userKey , username) values('%s','%s')" %(key, username)
    print(sql)
    cursor.execute(sql)
    db.commit()
    return key

def checkUserExist(key):
    sql = "select * from user where user.userKey = '%s'"%(key)
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        result = cursor.fetchone()
        if not result is None:
            return True
        else:
            return  False
    except:
        print("Error: unable to fetch data")
        return False


app = Flask(__name__)
@app.route('/register', methods=['POST'])
def post():

    if request.is_json :
        content = request.get_json()
        username = content["username"]
        ip = request.remote_addr
        key = register(username)

        return 'OK! Welcome %s! Your key is : %s .'%(username , key)
    else:
        return 'Json Error'


if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=5000)
    checkUserExist("4b3a07cc-123-11e8-9331-989096a534b2")
