import requests
import tkinter as tk
import time
from Weather import Weather
from Translate import Translate
from News import News
import urllib,  json


HEIGHT = 600
WIDTH = 1000
# 创建主界面
class MainWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("网络生活助手软件")
        self.canvas1 = tk.Canvas(self.window, height=HEIGHT, width=WIDTH)
        self.canvas1.pack()

        # frame6的布局（时间）
        self.f6 = tk.Frame(self.window, bg='#80c1ff', bd=5)
        self.f6.place(relx=0.5, rely=0.03, relwidth=0.3, relheight=0.1, anchor='n')
        self.L3 = tk.Label(self.f6, text='', fg='blue', font=("黑体", 40))
        self.L3.place(relx=0, rely=0, relwidth=1, relheight=1, anchor='nw')
        self.gettime()

        # 记录“天气”、“翻译”、“新闻”的value值
        self.var = tk.IntVar()
        # frame1的布局（天气）
        self.f1 = tk.Frame(self.window, bg='#80c1ff', bd=5)
        self.f1.place(relx=0.1, rely=0.15, relwidth=0.2, relheight=0.1, anchor='nw')
        self.R1 = tk.Radiobutton(self.f1, text="天气", width=200, variable=self.var,
                                 value=1, font=70, bg='#FF99FF', command=lambda : self.weather())
        self.R1.place(relx=0, rely=0, relwidth=1, relheight=1, anchor='nw')

        # frame2的布局（翻译）
        self.f2 = tk.Frame(self.window, bg='#80c1ff', bd=5)
        self.f2.place(relx=0.4, rely=0.15, relwidth=0.2, relheight=0.1, anchor='nw')
        self.R2 = tk.Radiobutton(self.f2, text="翻译", width=200, variable=self.var,
                                 value=2, font=70, bg='#FFFF00', command=lambda : self.trans())
        self.R2.place(relx=0, rely=0, relwidth=1, relheight=1, anchor='nw')

        # frame3的布局（新闻）
        self.f3 = tk.Frame(self.window, bg='#80c1ff', bd=5)
        self.f3.place(relx=0.7, rely=0.15, relwidth=0.2, relheight=0.1, anchor='nw')
        self.R3 = tk.Radiobutton(self.f3, text="新闻", width=200, variable=self.var,
                                 value=3, font=70, bg='#33ff33', command=lambda : self.news())
        self.R3.place(relx=0, rely=0, relwidth=1, relheight=1, anchor='nw')

        # frame7的布局（历史上的今天）
        self.count = -3
        self.f7 = tk.Frame(self.window, bg='#80c1ff', bd=5)
        self.f7.place(relx=0.5, rely=0.3, relwidth=0.42, relheight=0.55, anchor='nw')
        self.L4 = tk.Label(self.f7, text="历史上的今天", font=60, bg='#FFCC99', bd=5)
        self.L4.place(relx=0.5, rely=0, relwidth=0.6, relheight=0.15, anchor='n')
        self.b1 = tk.Button(self.f7, text="上一页", font=60, bd=5,
                            command=lambda: self.get_today_previous())
        self.b1.place(relx=0, rely=0, relwidth=0.18, relheight=0.15, anchor='nw')
        self.b2 = tk.Button(self.f7, text="下一页", font=60, bd=5,
                            command=lambda: self.get_today_next())
        self.b2.place(relx=0.82, rely=0, relwidth=0.18, relheight=0.15, anchor='nw')
        self.L5 = tk.Label(self.f7, font=60, bd=5, justify='left')
        self.L5.place(relx=0, rely=0.18, relwidth=1, relheight=0.8, anchor='nw')
        self.get_today_next()

        # frame8的布局（每日一句）
        self.f8 = tk.Frame(self.window, bg='#80c1ff', bd=0)
        self.f8.place(relx=0.5, rely=0.88, relwidth=0.55, relheight=0.1, anchor='n')
        self.L6 = tk.Label(self.f8, font=60, bd=5, fg='#9900CC', justify='right')
        self.L6.place(relx=0, rely=0, relwidth=1, relheight=1, anchor='nw')
        self.yiyan()

        # frame5的布局（日历标题）
        self.f5 = tk.Frame(self.window, bg='#80c1ff', bd=5)
        self.f5.place(relx=0.05, rely=0.3, relwidth=0.42, relheight=0.09, anchor='nw')
        self.L1 = tk.Label(self.f5, text="万年历", font=60, bg='#FFCC99', bd=5)
        self.L1.place(relx=0, rely=0, relwidth=1, relheight=1, anchor='nw')

        # frame4的布局（日历）
        self.f4 = tk.Frame(self.window, bg='#80c1ff', bd=5)
        self.f4.place(relx=0.05, rely=0.4, relwidth=0.42, relheight=0.45, anchor='nw')
        self.L2 = tk.Label(self.f4, text="", font=60, bg='#F0F0F0', bd=5)
        self.L2.place(relx=0, rely=0, relwidth=1, relheight=1, anchor='nw')

## 创建万年历 line86-line189
        '''添加日历头'''
        # 得到当前的日期，设置为默认值
        now = time.localtime(time.time())
        col_idx = 0

        # 创建年份组件
        self.vYear = tk.StringVar()
        self.vYear.set(now[0])
        tk.Label(self.f4, text='年').grid(row=0, column=col_idx);
        col_idx += 1
        # 设置年份可选菜单OptionMenu项，OptionMenu功能与combox相似
        omYear = tk.OptionMenu(self.f4, self.vYear, *tuple(range(1900, 2051)))
        omYear.grid(row=0, column=col_idx);
        col_idx += 1

        # 创建月份组件
        self.vMonth = tk.StringVar()
        self.vMonth.set(now[1])
        tk.Label(self.f4, text='月').grid(row=0, column=col_idx);
        col_idx += 1
        # 设置月份可选菜单OptionMenu项
        omMonth = tk.OptionMenu(self.f4, self.vMonth, *tuple(range(1, 13)))
        omMonth.grid(row=0, column=col_idx);
        col_idx += 1

        # 创建日组件
        self.vDay = tk.StringVar()
        self.vDay.set(now[2])
        tk.Label(self.f4, text='日').grid(row=0, column=col_idx);
        col_idx += 1
        # 设置日可选菜单OptionMenu项
        omDay = tk.OptionMenu(self.f4, self.vDay, *tuple(range(1, 32)))
        omDay.grid(row=0, column=col_idx);
        col_idx += 1

        # 创建空日历
        for i in range(6):
            for j in range(7):
                tk.Label(self.f4, text='').grid(row=i + 2, column=j)

        # 得到当月的日期分布并显示在页面上
        self.updateDate()

        # 创建更新按钮
        btUpdate = tk.Button(self.f4, text='更新日历', command=self.updateDate)
        btUpdate.grid(row=0, column=col_idx);
        col_idx += 1

        # 打印星期标签
        weeks = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
        for week in weeks:
            tk.Label(self.f4, text=week).grid(row=1, column=weeks.index(week))

    # 更新日历
    def updateDate(self):
        # 得到当前选择的日期
        year = int(self.vYear.get())
        month = int(self.vMonth.get())
        day = int(self.vDay.get())
        fd = self.calcFirstDayOfMonth(year, month, day)
        print(fd)
        # fd=2
        for i in range(6):
            for j in range(7):
                # 返回 grid 中 (i +2,j)位置的组件
                self.f4.grid_slaves(i + 2, j)[0]['text'] = ''
        # 计算本月的天数
        days = self.year_days(year, month)
        for i in range(1, days + 1):
            self.f4.grid_slaves(int((i + fd - 1) // 7 + 2), (i + fd - 1) % 7)[0]['text'] = str(i)

    # 获取总天数
    def get_total_days(self, year, month, day):
        total_days = 0
        for m in range(1800, year):
            if self.leap_year(m) == True:
                total_days += 366
            else:
                total_days += 365
        for i in range(1, month):
            total_days += self.year_days(year, i)
        return total_days


    def calcFirstDayOfMonth(self, year, month, day):
        # 返回当月1日是星期几，由1800.01.01是星期三推算
        return (self.get_total_days(year, month, day) + 3) % 7

    def year_days(self, year, month):  # 计算本月天数
        if month in (1, 3, 5, 7, 8, 10, 12):
            return 31
        elif month in (4, 6, 9, 11):
            return 30
        else:
            if self.leap_year(year) == True:
                return 29
            else:
                return 28

    def leap_year(self, year):
        # 判断是否为闰年
        if (year % 400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):
            return True
        else:
            return False

    # 获取当前时间函数，布局在frame6上
    def gettime(self):
        timestr = time.strftime("%H:%M:%S")  # 获取当前的时间并转化为字符串
        self.L3.configure(text=timestr)  # 重新设置标签文本
        self.f6.after(1000, self.gettime)  # 每隔1s调用函数 gettime 自身获取时间

    # 历史上的今天格式(上一页)
    def format_today_previous(self, today_previous):
        try:
            # 换页条件
            if len(today_previous['result'])%3 != 0:
                if 0 < self.count <= len(today_previous['result'])-len(today_previous['result'])%3:
                    self.count = self.count - 3
                else:
                    self.count = 0
            else:
                if 0 < self.count <= len(today_previous['result'])-3:
                    self.count = self.count - 3
                else:
                    self.count = 0

            # # test换页
            # if len(today_previous['result'])%3 != 0:
            #     if 0 < self.count <= len(today_previous['result'])-len(today_previous['result'])%3:
            #         self.count = self.count - 3
            #     else:
            #         self.count = len(today_previous['result'])-len(today_previous['result'])%3
            # else:
            #     if 0 < self.count <= len(today_previous['result'])-3:
            #         self.count = self.count - 3
            #     else:
            #         self.count = len(today_previous['result'])-3


            # 返回三条信息(多行时学会用列表与循环)
            if len(today_previous['result'])%3 == 0:
                date1 = today_previous['result'][self.count]['date']
                title1 = today_previous['result'][self.count]['title']
                date2 = today_previous['result'][self.count + 1]['date']
                title2 = today_previous['result'][self.count + 1]['title']
                date3 = today_previous['result'][self.count + 2]['date']
                title3 = today_previous['result'][self.count + 2]['title']
            elif len(today_previous['result'])%3 == 1:
                date1 = today_previous['result'][self.count]['date']
                title1 = today_previous['result'][self.count]['title']
                if (self.count + 1) > len(today_previous['result'])-1:
                    date2 = ''
                    title2 = ''
                else:
                    date2 = today_previous['result'][self.count + 1]['date']
                    title2 = today_previous['result'][self.count + 1]['title']

                if (self.count + 2) > len(today_previous['result'])-1:
                    date3 = ''
                    title3 = ''
                else:
                    date3 = today_previous['result'][self.count + 2]['date']
                    title3 = today_previous['result'][self.count + 2]['title']

            elif len(today_previous['result']) % 3 == 2:
                date1 = today_previous['result'][self.count]['date']
                title1 = today_previous['result'][self.count]['title']
                date2 = today_previous['result'][self.count + 1]['date']
                title2 = today_previous['result'][self.count + 1]['title']
                if (self.count + 2) > len(today_previous['result'])-1:
                    date3 = ''
                    title3 = ''
                else:
                    date3 = today_previous['result'][self.count + 2]['date']
                    title3 = today_previous['result'][self.count + 2]['title']
            else:
                print('error')


            # 当title的一行超过17词时，执行换行操作
            if len(title1) >= 17:
                row_title1 = int(len(title1) / 17)
                list_title1 = list(title1)
                for i_title1 in range(row_title1):
                    list_title1.insert(17 + (17 + 1) * i_title1, '\n      ')
                after_title1 = ''.join(list_title1)
                after_title1 = str(after_title1)
            else:
                after_title1 = title1
            # print(after_title1)

            if len(title2) >= 17:
                row_title2 = int(len(title2) / 17)
                list_title2 = list(title2)
                for i_title2 in range(row_title2):
                    list_title2.insert(17 + (17 + 1) * i_title2, '\n      ')
                after_title2 = ''.join(list_title2)
                after_title2 = str(after_title2)
            else:
                after_title2 = title2
            # print(after_title2)

            if len(title3) >= 17:
                row_title3 = int(len(title3) / 17)
                list_title3 = list(title3)
                for i_title3 in range(row_title3):
                    list_title3.insert(17 + (17 + 1) * i_title3, '\n      ')
                after_title3 = ''.join(list_title3)
                after_title3 = str(after_title3)
            else:
                after_title3 = title3
            # print(after_title3)

            # 输出格式设置
            if (date1 and date2 and date3) != '':
                # print(1)
                pretoday_str = '时间: %s\n事件: %s\n\n时间: %s\n事件: %s\n\n时间: %s\n事件: %s\n' \
                                % (date1, after_title1, date2, after_title2, date3, after_title3)

            elif date2 == '' and date3 == '' and date1 != '':
                # print(2)
                pretoday_str = '时间: %s\n事件: %s' % (date1, after_title1)

            elif date3 == '' and date1 != '' and date2 != '':
                # print(3)
                pretoday_str = '时间: %s\n事件: %s\n\n时间: %s\n事件: %s\n\n' % \
                                (date1, after_title1, date2, after_title2)

            else:
                print('error')
        except:
            pretoday_str = 'There was a problem retrieving that information'

        return pretoday_str


    # 历史上的今天格式(首页以及下一页)
    def format_today_next(self, today_next):
        try:
            # 换页条件
            if len(today_next['result'])%3 != 0:
                if self.count < len(today_next['result'])-len(today_next['result'])%3:
                    self.count = self.count + 3
            elif len(today_next['result'])%3 == 0:
                if self.count < len(today_next['result'])-3:
                    self.count = self.count + 3

            # # test换页
            # if len(today_next['result'])%3 != 0:
            #     if self.count < len(today_next['result'])-len(today_next['result'])%3:
            #         self.count = self.count + 3
            #     else:
            #         self.count = 0
            # else:
            #     if self.count < len(today_next['result'])-3:
            #         self.count = self.count + 3
            #     else:
            #         self.count = 0



            # 返回三条信息
            if len(today_next['result'])%3 == 0:
                # print('text')
                date1 = today_next['result'][self.count]['date']
                title1 = today_next['result'][self.count]['title']
                date2 = today_next['result'][self.count + 1]['date']
                title2 = today_next['result'][self.count + 1]['title']
                date3 = today_next['result'][self.count + 2]['date']
                title3 = today_next['result'][self.count + 2]['title']
            elif len(today_next['result'])%3 == 1:
                # print(13)
                date1 = today_next['result'][self.count]['date']
                title1 = today_next['result'][self.count]['title']
                if (self.count + 1) > len(today_next['result'])-1:
                    date2 = ''
                    title2 = ''
                else:
                    date2 = today_next['result'][self.count + 1]['date']
                    title2 = today_next['result'][self.count + 1]['title']

                if (self.count + 2) > len(today_next['result'])-1:
                    date3 = ''
                    title3 = ''
                else:
                    date3 = today_next['result'][self.count + 2]['date']
                    title3 = today_next['result'][self.count + 2]['title']

            elif len(today_next['result']) % 3 == 2:
                # print(14)
                date1 = today_next['result'][self.count]['date']
                title1 = today_next['result'][self.count]['title']
                date2 = today_next['result'][self.count + 1]['date']
                title2 = today_next['result'][self.count + 1]['title']
                if (self.count + 2) > len(today_next['result'])-1:
                    date3 = ''
                    title3 = ''
                else:
                    date3 = today_next['result'][self.count + 2]['date']
                    title3 = today_next['result'][self.count + 2]['title']
            else:
                print('error')

            # print(type(title1))


            # 当title的一行超过17个词数时，执行换行操作
            if len(title1) >= 17:
                row_title1 = int(len(title1)/17)
                list_title1 = list(title1)
                for i_title1 in range(row_title1):
                    list_title1.insert(17+(17+1)*i_title1, '\n      ')
                after_title1 = ''.join(list_title1)
                after_title1 = str(after_title1)
            else:
                after_title1 = title1
            # print(after_title1)

            if len(title2) >= 17:
                row_title2 = int(len(title2)/17)
                list_title2 = list(title2)
                for i_title2 in range(row_title2):
                    list_title2.insert(17+(17+1)*i_title2, '\n      ')
                after_title2 = ''.join(list_title2)
                after_title2 = str(after_title2)
            else:
                after_title2 = title2
            # print(after_title2)

            if len(title3) >= 17:
                row_title3 = int(len(title3)/17)
                list_title3 = list(title3)
                # print(list_title3)
                for i_title3 in range(row_title3):
                    list_title3.insert(17+(17+1)*i_title3, '\n      ')
                after_title3 = ''.join(list_title3)
                after_title3 = str(after_title3)
            else:
                after_title3 = title3
            # print(after_title3)

            # 输出格式设置
            if (date1 and date2 and date3) != '':
                # print(1)
                nexttoday_str = '时间: %s\n事件: %s\n\n时间: %s\n事件: %s\n\n时间: %s\n事件: %s\n' \
                            % (date1, after_title1, date2, after_title2, date3, after_title3)

            elif date2 == '' and date3 == '' and date1 != '':
                # print(2)
                nexttoday_str = '时间: %s\n事件: %s' % (date1, after_title1)

            elif date3 == '' and date1 != '' and date2 != '':
                # print(3)
                nexttoday_str = '时间: %s\n事件: %s\n\n时间: %s\n事件: %s\n\n' % \
                                (date1, after_title1, date2, after_title2)


            else:
                print('error')
        except:
            nexttoday_str = 'There was a problem retrieving that information'

        return nexttoday_str

        # 历史上的今天(上一页)
    def get_today_previous(self):
        url = 'https://api.oick.cn/lishi/api.php'
        response_previous = requests.get(url)
        today_previous = response_previous.json()
        # print(today_previous)
        self.L5['text'] = self.format_today_previous(today_previous)


    # 历史上的今天(首页以及下一页)
    def get_today_next(self):
        url = 'https://api.oick.cn/lishi/api.php'
        response_next = requests.get(url)
        today_next = response_next.json()
        # print(today_next)
        self.L5['text'] = self.format_today_next(today_next)


    # 每日一句格式
    def format_yiyan(self, yiyan):
        try:
            context = yiyan['hitokoto']
            fromwho = yiyan['from_who']

            yiyan_str = '%s \n           --%s' % (context, fromwho)

        except:
            yiyan_str = 'There was a problem retrieving that information'

        return yiyan_str

    # 每日一句
    def yiyan(self):
        url = 'https://v1.hitokoto.cn/?c=i'
        response = requests.get(url)
        yiyan = response.json()
        # print(yiyan)
        self.L6['text'] = self.format_yiyan(yiyan)

    # 天气子窗口
    def weather(self):
        Weather(self.window)


    # 翻译子窗口
    def trans(self):
        Translate(self.window)

    # 新闻子窗口
    def news(self):
        News(self.window)


# 产生主窗口
window = tk.Tk()
p1 = MainWindow(window)
window.mainloop()