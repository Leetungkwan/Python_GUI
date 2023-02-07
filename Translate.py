import tkinter as tk
import requests
from tkinter import ttk


class Translate:
    def __init__(self, window):
        self.window = window
        self.window = tk.Toplevel(self.window)
        self.window.title('翻译')

        self.canvas = tk.Canvas(self.window, height=700, width=800)
        self.canvas.pack()

        # 选择按键布局
        self.f1 = tk.Frame(self.window, bd=5)
        self.f1.place(relx=0.5, rely=0.05, relwidth=0.75, relheight=0.07, anchor='n')
        self.transvar1 = tk.StringVar()
        self.transvar1.set('自动')
        self.transvar2 = tk.StringVar()
        self.transvar2.set('自动')
        self.transvalues = ['自动', '中文', '英文', '日文', '韩文', '法文', '西班牙文', '葡萄牙文', '意大利文', '俄文', '乌兹别克语']
        self.c1 = ttk.Combobox(self.f1, textvariable=self.transvar1, values=self.transvalues, state='normal',
                               font=('宋体', 13))
        self.c1.place(relx=0.11, rely=0, relwidth=0.22, relheight=1, anchor='nw')
        self.L2 = tk.Label(self.f1, text='翻译为', font=10, bd=5)
        self.L2.place(relx=0.4, rely=0, relwidth=0.2, relheight=1, anchor='nw')
        self.c2 = ttk.Combobox(self.f1, textvariable=self.transvar2, values=self.transvalues, state='normal',
                               font=('宋体', 13))
        self.c2.place(relx=0.68, rely=0, relwidth=0.22, relheight=1, anchor='nw')
        # 绑定选中事件，当一窗口显示非自动和中文外的语言时，二窗口显示中文
        self.c1.bind('<<ComboboxSelected>>', self.choose1)
        # 绑定选中事件，当二窗口显示非自动和中文外的语言时，一窗口显示中文
        self.c2.bind('<<ComboboxSelected>>', self.choose2)

        self.f2 = tk.Frame(self.window, bg='#80c1ff', bd=5)
        self.f2.place(relx=0.5, rely=0.2, relwidth=0.9, relheight=0.1, anchor='n')

        self.e1 = tk.Entry(self.f2, font=40)
        self.e1.place(relwidth=0.8, relheight=1)

        self.b1 = tk.Button(self.f2, text="翻译", font=40, command=lambda : self.get_trans(self.e1.get()))
        self.b1.place(relx=0.85, relheight=1, relwidth=0.15)

        self.f3 = tk.Frame(self.window, bg='#80c1ff', bd=5)
        self.f3.place(relx=0.5, rely=0.35, relwidth=0.9, relheight=0.6, anchor='n')

        self.L1 = tk.Label(self.f3, bd=5, font=('黑体', 15), justify='left')
        self.L1.place(relwidth=1, relheight=1, anchor='nw')

        # print(self.c1.get())


    # 一窗口绑定事件
    def choose1(self, event):
        widget = event.widget
        value = widget.get()
        if value != '自动' and '中文':
            self.c2.set('中文')

    # 二窗口绑定事件
    def choose2(self, event):
        widget = event.widget
        value = widget.get()
        if value != '自动' and '中文':
            self.c1.set('中文')

    # 翻译获取函数
    def get_trans(self, origin):
        Q = origin
        if Q == '':
            self.L1['text'] = '输入不能为空'
        From = self.c1.get()
        To = self.c2.get()
        params_trans = {
            'q' : Q,
            'from' : From,
            'to' : To
         }
        trans = requests.get('https://aidemo.youdao.com/trans',params=params_trans)
        trans_json = trans.json()
        trans_text = trans_json['translation'][0]
        # print(type(trans_text))

        if len(trans_text) >= 25:
            row_trans_text = int(len(trans_text) / 25)
            list_trans_text = list(trans_text)
            # print(list_trans_text)
            for i_trans_text in range(row_trans_text):
                list_trans_text.insert(30 + (30 + 1) * i_trans_text, '\n')
            after_trans_text = ''.join(list_trans_text)
            after_trans_text = str(after_trans_text)
        else:
            after_trans_text = trans_text

        self.L1['text'] = after_trans_text


# 测试函数
if __name__ == '__main__':
	window = tk.Tk()
	translate = Translate(window)
	window.mainloop()