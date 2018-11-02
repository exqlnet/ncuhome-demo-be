from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config["SQLALCHEMY_DATABASE_URI"] = r"sqlite:///.\demo.db"

db = SQLAlchemy(app)


@app.before_request
def app_before_request():
    print("HTTP {}  {}".format(request.method, request.url))


@app.after_request
def app_after_request(response):
    response.headers["From"] = "Ncuhome"
    return response


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True)  # 用户名
    desc = db.Column(db.String(256))  # 用户描述信息


db.create_all()


@app.route("/add", methods=['POST'])
def add():
    """
    添加一个用户
    :return:
    """
    username = request.json.get("username")
    desc = request.json.get("desc")

    if not username or not desc:
        return jsonify({
                "status": 0,
                "message": "提交信息有误！"
             }), 400

    # 检查用户是否已经存在
    check_user = User.query.filter_by(username=username).first()
    if check_user:
        return jsonify({
            "status": 0,
            "message": "用户已存在！"
        })

    # 创建用户
    user = User(username=username, desc=desc)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "status": 1,
        "message": "用户{}添加成功！".format(username)
    }), 200


@app.route("/delete", methods=['DELETE'])
def delete():
    """
    删除用户
    :return:
    """
    username = request.json.get("username")
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()

    return jsonify({
        "status": 1,
        "message": "用户{}删除成功！".format(username)
    }), 200


@app.route("/get", methods=['GET'])
def get_user():
    """
    获取用户信息
    :return:
    """
    username = request.args.get("username")
    if not username:
        abort(400)
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({
            "status": 0,
            "message": "未找到用户！"
        }), 404

    return jsonify({
        "status": 1,
        "message": "获取成功",
        "data": {
            "username": user.username,
            "desc": user.desc,
        }})


@app.route("/change_desc", methods=["PUT"])
def change_desc():
    """
    修改描述信息
    :return:
    """
    username = request.json.get("username")
    desc = request.json.get("desc")
    if not username:
        return jsonify({
                "status": 0,
                "message": "提交信息有误！"
             }), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({
                "status": 0,
                "message": "未找到用户！"
            }), 404

    user.desc = desc
    db.session.commit()
    return jsonify({
        "status": 1,
        "message": "描述修改成功！"
    })


@app.route("/list", methods=["GET"])
def user_list():
    users = User.query.all()
    data = []
    for user in users:
        data.append({
            "user_id": user.user_id,
            "username": user.username,
            "desc": user.desc,
        })
    return jsonify(data)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
