import os, time, threading, tkinter
import time
import threading
import os.path
import flask
from datetime import datetime
from flask import request, jsonify
import json
from flask import send_file

app = flask.Flask(__name__)

@app.route("/")
def nonepage():
    return flask.redirect("/index.html")


@app.route("/<path:page>")
def mainpage(page):
    if os.path.isdir(page):
        page += "/index.html"
    return send_file(page)


def verify_password(username, password):
    user_dir = os.path.join("users", username)
    user_file = os.path.join(user_dir, "user.json")

    if os.path.exists(user_file):
        with open(user_file, "r", encoding="UTF-8") as f:
            user_data = json.load(f)
            if password == user_data["password"]:
                return True

    return False

def update_last_login_time(username):
    user_dir = os.path.join("users", username)
    user_file = os.path.join(user_dir, "user.json")

    if os.path.exists(user_file):
        with open(user_file, "r+", encoding="UTF-8") as f:
            user_data = json.load(f)
            user_data["last_login_time"] = str(datetime.now())
            f.seek(0)
            json.dump(user_data, f, indent=4)
            f.truncate()
from flask import make_response
@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    if not username or not password:
        return jsonify({"type": "error", "code": 400, "error": "用户名和密码不能为空!"}), 400

    if verify_password(username, password):
        response = make_response(jsonify({"type": "success", "message": "登录成功"}))
        response.set_cookie('loggedIn', 'True')  # 设置登录状态的Cookie
        response.set_cookie('loginText', '个人主页')  # 设置按钮文字的Cookie
        return response, 200
    else:
        return jsonify({"type": "error", "code": 401, "error": "密码不正确"}), 401


import time
from collections import defaultdict
ip_register_time = defaultdict(float)

prohibited_words = ["admin", "Administrator", "administrator", "官方", "官 方", "傻 逼", "病", "死", "妈", "脑瘫", "脑残", "傻逼", "sb"]
@app.route("/api/register", methods=['POST'])
def registerP():
    if not os.path.exists("users"):
        os.makedirs("users")
    ip = request.remote_addr

    if ip in ip_register_time:
        return jsonify({"type": "error", "code": "", "error": "1009", "message": "同一IP只能注册一个账号！"})

    current_time = time.time()
    if current_time - ip_register_time[ip] < 30:
        return jsonify({"type": "error", "code": "", "error": "1010", "message": "请求频繁！请30秒后再进行注册请求！"})

    ip_register_time[ip] = current_time
    data = request.json
    if not data:
        return jsonify({"type": "error", "code": "", "error": "1000", "message": "请求数据为空！"})

    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify({"type": "error", "code": "", "error": "1001", "message": "用户名不能为空！"})
    if any(word in username for word in prohibited_words):
        return jsonify({"type": "error", "code": "", "error": "1008", "message": "用户名含有违禁词！"})

    if not password:
        return jsonify({"type": "error", "code": "", "error": "1002", "message": "密码不能为空！"})

    if os.path.exists("users/" + username):
        return jsonify({"type": "error", "code": "", "error": "1007", "message": "用户名已存在！"})

    user_count = len(os.listdir('users'))
    new_id = str(user_count + 1)

    user_dir = os.path.join("users", username)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    user_file = os.path.join(user_dir, "user.json")
    user = {
        "id": new_id,
        "username": username,
        "password": password,
    }

    with open(user_file, "w", encoding="UTF-8") as f:
        json.dump(user, f)

    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{username} 的主页</title>
    </head>
 <body>
   <h2>欢迎来到{username}的主页</h2>
</body>
</html>
    """.format(username=data["username"], id=new_id)

    with open(os.path.join(user_dir, "index.html"), "w", encoding="UTF-8") as f:
        f.write(html_content)

    return make_response(jsonify({"type": "OK", "error": "", "code": new_id, "message": "注册成功！"}))


def onserver():
    global w
    time.sleep(0.5)
    os.system("cls")
    print("欢迎使用©DAIQITAO-v2.0网站服务端。")
    print("服务端已准备就绪！\n开始记录日志：\n")

    w = tkinter.Tk()
    w.title("")
    e = tkinter.Entry(w, font=["Consolas", 10, ""])
    e.pack()
    b1 = tkinter.Button(
        w,
        text="Enter CMD",
        command=lambda: os.system(e.get()),
        font=["Consolas", 10, ""],
    )
    b2 = tkinter.Button(
        w, text="Enter CPY", command=lambda: exec(e.get()), font=["Consolas", 10, ""]
    )
    b1.pack()
    b2.pack()
    w.mainloop()


threading.Thread(target=onserver).start()
app.run(host="0.0.0.0", port=5000)
print("服务端已停止运行。\n")
w.destroy()