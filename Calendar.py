from tkinter import *
import time

class Calendar:
    def __init__(self):
        self.vYear = StringVar()
        self.vMonth = StringVar()
        self.vDay = StringVar()
        self.vNongLi = StringVar()

    def leap_year(self,year):
        #判断是否为闰年
        if (year %400 == 0) or ((year % 4 == 0) and (year % 100 != 0)):
            return True
        else:
            return False
    def year_days(self,year,month):  #计算本月天数
        if month in (1,3,5,7,8,10,12):
            return 31
        elif month in (4,6,9,11):
            return 30
        else:
            if self.leap_year(year)==True:
                return 29
            else:
                return 28

    def get_total_days(self,year,month,day):
        # 计算一年的天数
        total_days=0
        for m in range(1800,year):
            if self.leap_year(m)==True:
                total_days+=366
            else:
                total_days+=365
        for i in range(1,month):
            total_days+=self.year_days(year,i)
        return total_days

    def calcFirstDayOfMonth(self,year,month,day):
        #返回当月1日是星期几，由1800.01.01是星期三推算
        return(self.get_total_days(year,month,day)+3)%7


    def createMonth(self,master):
            #创建日历
        for i in range(6):
            for j in range(7):
                Label(master,text='').grid(row = i + 2,column = j)

    #更新日历
    def updateDate(self):
        #得到当前选择的日期
        year = int(self.vYear.get())
        month = int(self.vMonth.get())
        day = int(self.vDay.get())
        fd = self.calcFirstDayOfMonth(year,month,1)
        print(fd)
        #fd=2
        for i in range(6):
            for j in range(7):
                #返回 grid 中 (i +2,j)位置的组件
                root.grid_slaves(i +2,j)[0]['text'] = ''
        #计算本月的天数
        days=self.year_days(year,month)
        for i in range(1,days + 1):
            root.grid_slaves(int((i + fd - 1)//7 + 2),(i + fd -1)%7)[0]['text'] = str(i)

    def drawHeader(self,master):
        '''添加日历头'''
        #得到当前的日期，设置为默认值
        now = time.localtime(time.time())
        col_idx = 0

        #创建年份组件
        self.vYear = StringVar()
        self.vYear.set(now[0])
        Label(master,text = '年').grid(row = 0,column = col_idx);col_idx += 1
        #设置年份可选菜单OptionMenu项，OptionMenu功能与combox相似
        omYear = OptionMenu(master,self.vYear,*tuple(range(1900,2051)))
        omYear.grid(row = 0,column = col_idx);col_idx += 1

        #创建月份组件
        self.vMonth.set(now[1])
        Label(master,text = '月').grid(row = 0,column = col_idx);col_idx += 1
        #设置月份可选菜单OptionMenu项
        omMonth = OptionMenu(master,self.vMonth,*tuple(range(1,13)))
        omMonth.grid(row = 0,column = col_idx);col_idx += 1

        #创建日组件
        self.vDay.set(now[2])
        Label(master,text = '日').grid(row = 0,column = col_idx);col_idx +=1

        #设置日可选菜单OptionMenu项
        omDay = OptionMenu(master,self.vDay,*tuple(range(1,32)))
        omDay.grid(row = 0,column = col_idx);col_idx += 1

        #创建更新按钮
        btUpdate=Button(master,text = '更新日历',command = self.updateDate)
        btUpdate.grid(row = 0,column = col_idx);col_idx += 1


        #打印星期标签
        weeks = ['周日','周一','周二','周三','周四','周五','周六']
        for week in weeks:
            Label(master,text = week).grid(row = 1,column = weeks.index(week))


root = Tk()
root.title("万年历")
AppCal=Calendar()
AppCal.drawHeader(root)
AppCal.createMonth(root)
AppCal.updateDate()
root.mainloop()
