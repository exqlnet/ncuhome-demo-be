from flask import Flask, request, redirect, abort, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<b style='color: red'>Hello World!</b>"


@app.route('/hello/<string:name>')
def hello(name):
    return render_template('index.html', name=name)


@app.route('/ncuos')
def ncuos():
    return redirect("https://www.ncuos.com/")


@app.route('/user/<int:user_id>', methods=['GET'])
def user(user_id):
    if not user_id == 1:
        abort(404)

    return jsonify({
        "status": 1,
        "data": {
            "username": "admin",
            "password": "123456",
        },
        "message": "获取成功"
    })


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if not (username == "admin" and password == "123456"):
        return jsonify({
            "status": 0,
            "message": "登陆失败",
        })

    return jsonify({
        "status": 1,
        "message": "登陆成功"
    })


if __name__ == '__main__':
    app.run()
