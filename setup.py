import pymysql
import datetime
import uuid
from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
import json

dbHost = ""
port = 3306
user = ""
pwd = ""
database = "UserSignIn"

db = pymysql.connect(host=dbHost, port=port, user=user, password=pwd, database=database)
cursor = db.cursor()

def register(username):
    key = uuid.uuid1()
    sql = "insert into user(userKey , username) values('%s','%s')" % (key, username)
    print(sql)
    cursor.execute(sql)
    db.commit()
    return str(key)


def checkUserExist(key):
    """

    :param key: user uuid key
    :return: True or False
    """
    sql = "select * from user where user.userKey = '%s'" % (key)
    print(sql)
    try:
        cursor.execute(sql)
        result = cursor.fetchone()
        if not result is None:
            return True
        else:
            return False
    except:
        print("Error: unable to fetch data")
        return False


def checkTodaySignIn(key):
    """

    :param key: userKey
    :return: 1:可以签到 0:今天已经签到 -1：用户不存在
    """
    if checkUserExist(key):
        sql = "select sign.time from sign where sign.userKey = '%s' and sign.date = '%s'" % (key, datetime.date.today())
        cursor.execute(sql)
        query_result = cursor.fetchone()
        if not query_result is None:
            print(query_result)
            return 0
        else:
            return 1
    return -1


def userSignIn(key):
    """
    :param key: userKey
    :return:
    """
    result = checkTodaySignIn(key)
    if result == 1:
        sql = "insert into sign(userKey ,time ,date) values('%s' , '%s' , '%s')" % (
        key, datetime.datetime.today(), datetime.date.today())
        cursor.execute(sql)
        db.commit()
    return result


def TodaySignCount():
    """

    :return: 返回今日签到人数 int
    """
    sql = "select count(*) from sign where sign.date = '%s'" % datetime.date.today()
    cursor.execute(sql)
    return cursor.fetchone()[0]


def userSignCount(key):
    """

    :param key: userKey
    :return: 用户签到次数 int   -1:用户不存在
    """
    if checkUserExist(key):
        sql = "select count(*) from sign where sign.userKey = '%s'" % key
        cursor.execute(sql)
        return cursor.fetchone()[0]
    else:
        return -1


app = Flask(__name__)


@app.route('/register', methods=['GET'])
def url_register():
    username = request.args.get("username")
    if username is None:
        abort(404)
    # ip = request.remote_addr
    key = register(username)
    dict = {'key': key}
    return_json = json.dumps(dict)
    return jsonify(return_json)


@app.route('/sign', methods=['POST'])
def url_sign():
    if request.is_json:
        try:
            content = request.get_json()
            key = content["userKey"]
            dict = {'status': userSignIn(key)}
            return_json = json.dumps(dict)
            return jsonify(return_json)
        except:
            return "Json Key Error"

    else:
        return 'Json Error'


@app.route('/TodaySign', methods=['GET'])
def url_todaySign():
    dict = {'count': TodaySignCount()}
    return jsonify(json.dumps(dict))


@app.route('/userSign', methods=['POST'])
def url_userSign():
    if request.is_json:
        request_json = request.get_json()
        try:
            key = request_json["userKey"]
            result = userSignCount(key)
            dict = {'count': result}
            return jsonify(json.dumps(dict))
        except:
            return "Json Key Error"
    else:
        return "Json Error"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    # # checkUserExist("4b3a07cc-123-11e8-9331-989096a534b2")
    # checkTodaySignIn("4b3a07cc-f2d2-11e8-9331-989096a534b2")
