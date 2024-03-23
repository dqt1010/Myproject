import tkinter as tk
from tkinter import messagebox
import requests
import schedule

def sign_in(api_key):
    url = "https://api.v2.rainyun.com/user/reward/tasks"
    data = {"task_name": "每日签到"}
    headers = {
        "x-api-key": api_key,
        "User-Agent": "curl",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "Host": "api.v2.rainyun.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        messagebox.showinfo("签到成功", "签到成功！")
    else:
        messagebox.showerror("签到失败", "签到失败，请重试！")

def save_api_key(api_key_entry):
    api_key = api_key_entry.get()
    with open("api_key.txt", 'w') as file:
        file.write(api_key)
    messagebox.showinfo("保存成功", "API Key 已保存！")

def read_api_key_from_file(file_path, api_key_entry):
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip()
            api_key_entry.insert(0, api_key)
    except FileNotFoundError:
        messagebox.showerror("错误", "找不到API Key文件！")

def on_submit(api_key_entry):
    api_key = api_key_entry.get()
    sign_in(api_key)
    # 设置每天自动签到定时器
    schedule.every().day.at("08:00:00").do(sign_in, api_key)

# 创建 GUI 界面
root = tk.Tk()
root.title("Rainyun 自动签到")
root.geometry("400x200")

api_key_label = tk.Label(root, text="API Key:")
api_key_label.pack()

api_key_entry = tk.Entry(root, width=40)
api_key_entry.pack()

save_button = tk.Button(root, text="保存", command=lambda: save_api_key(api_key_entry))
save_button.pack()

read_api_key_from_file("api_key.txt", api_key_entry)

submit_button = tk.Button(root, text="签到", command=lambda: on_submit(api_key_entry))
submit_button.pack()

root.mainloop()