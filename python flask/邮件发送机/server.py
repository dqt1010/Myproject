import smtplib
from email.mime.text import MIMEText
import os
import time
import threading
import os.path
import flask
from flask import send_file,request
from tkinter import Tk, Entry, Button

app = flask.Flask(__name__)
class EmailSender:
    def __init__(self):
        self.Host = "smtp.163.com"
        self.Sender = ""
        self.Password = ""
        self.ROOT = smtplib.SMTP()

    def Login(self):
        self.ROOT.connect(self.Host, 25)
        self.ROOT.login(self.Sender, self.Password)

    def Send(self, to, text, title):
        text = MIMEText(text, "plain", "UTF-8")
        text["Subject"] = title
        text["From"] = self.Sender
        text["To"] = to
        text = text.as_string()
        self.ROOT.sendmail(self.Sender, to, text)

    def Exit(self):
        self.ROOT.quit()



def create_window():
    global w
    w = Tk()
    w.title("Flask GUI")
    e = Entry(w, font=["Consolas", 10, ""])
    e.pack()
    b1 = Button(
        w,
        text="Enter CMD",
        command=lambda: os.system(e.get()),
        font=["Consolas", 10, ""],
    )
    b2 = Button(
        w, text="Enter CPY", command=lambda: exec(e.get()), font=["Consolas", 10, ""]
    )
    b1.pack()
    b2.pack()
    w.mainloop()



@app.route("/")
def nonepage():
    return flask.redirect("/index.html")


@app.route("/<path:page>")
def mainpage(page):
    if os.path.isdir(page):
        page += "/index.html"
    return send_file(page)


@app.route("/api/sendEmail", methods=["POST"])
def sepage():
    args = request.form
    sender = EmailSender()
    sender.Sender = args["sender"]
    sender.Password = args["loginpwd"]
    sender.Login()
    sender.Send(args["target"], args["text"], args["title"])
    sender.Exit()



def onserver():
    global w
    time.sleep(0.5)
    os.system("cls")
    print("欢迎使用 ©DAIQITAO-v2.0 服务端。")
    print("服务端已准备就绪！\n开始记录日志：\n")

    threading.Thread(target=create_window).start()

    app.run(host="0.0.0.0", port=8080)
    print("服务端已停止运行。\n")
    if 'w' in globals():
        w.destroy()


if __name__ == "__main__":
    threading.Thread(target=onserver).start()