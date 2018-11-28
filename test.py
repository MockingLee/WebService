import pymysql
import datetime
import uuid
from flask import Flask
from flask import request

db = pymysql.connect(host = "jp.pkmgtdz.xyz" , port = 3306 , user = "ljx" , password = "lijixuan" , database = "UserSignIn")
cursor = db.cursor()

# x = uuid.uuid1()
# print(x.get_node())

def register(username):
    sql = "insert into user(userKey , username) values('%s','%s')" %(uuid.uuid1() , username)
    print(sql)
    cursor.execute(sql)
    db.commit()

app = Flask(__name__)
@app.route('/register', methods=['POST'])
def post():
    if request.is_json :
        content = request.get_json()
        username = content["username"]
        ip = request.remote_addr
        register(username)
        return 'OK! Welcome %s!'%username
    else:
        return 'Json Error'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
