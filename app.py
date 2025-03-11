import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
import openai

class FineTuneApp:
    def __init__(self, root):
        self.root = root
        self.root.title('微信聊天记录GPT微调工具')

        self.file_path = tk.StringVar()
        self.api_key = tk.StringVar()
        self.file_id = tk.StringVar()
        self.job_id = tk.StringVar()
        self.model_name = tk.StringVar()

        # 文件选择区域（可编辑显示路径）
        tk.Label(root, text="1. 选择聊天记录(txt)").pack(pady=5)
        
        file_frame = tk.Frame(root)
        self.file_entry_var = tk.StringVar()
        self.file_entry = tk.Entry(file_frame, textvariable=self.file_entry_var, width=60)
        self.file_entry.grid(row=0, column=0, padx=5)

        tk.Button(file_frame, text="浏览文件", command=self.select_file).grid(row=0, column=1)
        file_frame.pack(pady=5)

        # 显示并选择发言人姓名
        tk.Label(root, text="2. 模仿的用户名:").pack(pady=5)
        self.target_name_var = tk.StringVar()
        self.target_name_dropdown = tk.OptionMenu(root, self.target_name_var, '')
        self.target_name_dropdown.pack()

        # 数据转换按钮
        tk.Button(root, text="转换聊天记录为JSONL", command=self.convert_data).pack(pady=5)

        # 显示JSONL路径（不可编辑）
        tk.Label(root, text="转换后的文件路径:").pack()
        self.converted_entry_var = tk.StringVar()
        tk.Entry(root, textvariable=self.converted_entry_var, state='readonly', width=60).pack()

        # API输入框
        tk.Label(root, text="OpenAI API密钥:").pack(pady=5)
        tk.Entry(root, textvariable=self.api_key, width=60, show='*').pack()

        # 上传数据按钮
        tk.Button(root, text="上传数据文件", command=self.upload_file).pack(pady=5)
        tk.Label(root, text="数据文件ID:").pack()
        tk.Entry(root, textvariable=self.file_id, state='readonly', width=60).pack()

        # 启动微调任务
        tk.Button(root, text="启动微调模型任务", command=self.start_fine_tune).pack()
        tk.Label(root, text="微调任务ID:").pack()
        self.job_id_var = tk.StringVar()
        tk.Entry(root, textvariable=self.job_id_var, state='readonly', width=60).pack()

        # 状态监控
        tk.Label(root, text="任务状态:").pack()
        self.status_label = tk.Label(root, text="未开始", fg='blue')
        self.status_label.pack()

        # 训练完成模型名
        tk.Label(root, text="训练完成的模型名:").pack()
        tk.Entry(root, textvariable=self.model_name, state='readonly', width=60).pack()

        # 日志窗口
        tk.Label(root, text="日志输出:").pack(pady=5)
        self.log_text = tk.Text(root, height=10, state='disabled', wrap='word')
        self.log_text.pack(fill='both', padx=10, pady=5, expand=True)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.file_entry_var.set(file_path)
            self.file_path.set(file_path)
            self.log(f"已选择文件：{file_path}")

            # 读取文件获取用户名列表
            usernames = FineTuneApp.extract_usernames(file_path)
            if usernames:
                menu = self.target_name_dropdown["menu"]
                menu.delete(0, 'end')
                for name in usernames:
                    menu.add_command(label=name, command=lambda value=name: self.target_name_var.set(value))
                self.target_name_var.set(usernames[0])  # 默认选择第一个用户名
                self.log(f"识别到发言者：{', '.join(usernames)}")
            else:
                self.log("未找到任何发言者")

    def run_script_thread(self, target):
        threading.Thread(target=target, daemon=True).start()

    def convert_data(self):
        input_filename = self.file_entry_var.get()
        target_name = self.target_name_var.get()

        self.log("开始转换数据...")
        result = subprocess.run(
            ['python', 'convert_wechat.py', input_filename, target_name],
            capture_output=True, text=True
        )

        converted_path = result.stdout.strip()
        self.converted_entry_var.set(converted_path)
        self.log(f"转换成功，路径：{converted_path}")
        messagebox.showinfo("提示", f"数据转换成功！\n路径：{converted_path}")

    def upload_file(self):
        api_key = self.api_key.get()
        jsonl_path = self.converted_entry_var.get()
        
        self.log("开始上传文件...")
        result = subprocess.run(['python', 'upload_file.py', api_key, jsonl_path],capture_output=True, text=True)
        if result.returncode == 0:
            file_id = result.stdout.strip()
            self.file_id.set(file_id)
            self.log(f"文件上传成功，File ID: {file_id}")
        else:
            self.log(f"上传失败，错误：{result.stderr.strip()}")

    def start_fine_tune(self):
        self.log("启动微调任务...")
        self.status_label.config(text="进行中", fg='orange')
        result = subprocess.run(['python', 'start_finetune.py', self.api_key.get(), self.file_id.get()], capture_output=True, text=True)
        if result.returncode == 0:
            self.job_id = result.stdout.strip()
            self.status_label.config(text="进行中", fg='orange')
            self.log(f"微调任务已启动，Job ID: {result.stdout.strip()}")
            self.monitor_status()
        else:
            self.log(f"任务启动失败，错误：{result.stderr.strip()}")

    def monitor_status(self):
        def _monitor():
            self.log("开始监控微调状态...")
            while True:
                result = subprocess.run(['python', 'check_finetune_status.py', self.api_key.get(), self.job_id.get()], capture_output=True, text=True)
                status, model_name = result.stdout.strip().split(',')
                self.status_label.config(text=status)
                if status == "succeeded":
                    self.status_label.config(text="训练完毕", fg='green')
                    self.converted_entry_var.set(model_name)
                    break
                elif status in ['failed', 'cancelled']:
                    self.status_label.config(text="任务失败", fg='red')
                    break
                time.sleep(30)
        threading.Thread(target=_monitor, daemon=True).start()

    def log(self, message):
        self.log_text.config(state='normal')  # 可编辑状态
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)             # 自动滚动到底部
        self.log_text.config(state='disabled') # 回到不可编辑状态


def extract_usernames(filepath):
    import re
    usernames = set()
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} (.+)', line.strip())
            if match:
                usernames.add(match.group(1))
    return list(usernames)

FineTuneApp.extract_usernames = staticmethod(extract_usernames)

if __name__ == "__main__":
    import tkinter as tk
    import subprocess
    import threading
    import time

    root = tk.Tk()
    app = FineTuneApp(root)
    root.mainloop()



