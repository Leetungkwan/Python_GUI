import tkinter as tk
import urllib
import urllib.request
import urllib.parse
import json


class News:
	def __init__(self, window):
		self.window = window
		self.window = tk.Toplevel(window)
		self.window.title('新闻')

		# 一页中显示的新闻条数
		self.count = -3

		self.canvas = tk.Canvas(self.window, height=650, width=750)
		self.canvas.pack()

		# 单选按键的标志值
		self.news_var = tk.IntVar()

		# 单选按键的背景颜色
		self.news_color = ['#FF9999', '#FF99CC', '#FF0099', '#CC99FF', '#CC99CC',
						   '#FFCC00', '#FF6633', '#CC9933', '#CC6633', '#FF3333']

		# 单选按键的文本和value值
		self.news_value = [('头条', 0), ('社会', 1), ('国内', 2), ('国际', 3), ('娱乐', 4),
					   ('体育', 5), ('军事', 6), ('科技', 7), ('财经', 8), ('时尚', 9)]


		# 单选按键的背景布局列表
		self.button_frame = ['', '', '', '', '', '', '', '', '', '']

		# 单选按键的数量
		self.news_button = ['', '', '', '', '', '', '', '', '', '']

		# 创建单选按键
		button_count = 0
		for j_button_colum in range(2):
			for i_button_row in range(5):
				self.button_frame[button_count] = tk.Frame(self.window, bg='#80c1ff', bd=3)
				self.button_frame[button_count].place(relx=0.1 + 0.16 * i_button_row, rely=0.05 + 0.1 * j_button_colum,
													  relwidth=0.13, relheight=0.08, anchor='nw')
				self.news_button[button_count] = tk.Radiobutton(self.button_frame[button_count], width=100,
																value=button_count, variable=self.news_var,
																font=10, command=lambda : self.get_nextnews())
				self.news_button[button_count].place(relx=0, rely=0, relwidth=1, relheight=1, anchor='nw')
				button_count += 1

		for self.button_type, self.button_num in self.news_value:
			self.news_button[self.button_num]['text'] = self.button_type

		for i_color in range(10):
			self.news_button[i_color]['bg'] = self.news_color[i_color]

		# 创建文本框
		self.f11 = tk.Frame(self.window, bg='#80c1ff', bd=5)
		self.f11.place(relx=0.5, rely=0.24, relwidth=0.9, relheight=0.66, anchor='n')
		self.L1 = tk.Label(self.f11, font=('', 12), bd=5, justify='left')
		self.L1.place(relwidth=1, relheight=1, anchor='nw')


		# 创建上一页和下一页按键
		self.f12 = tk.Frame(self.window, bd=0)
		self.f12.place(relx=0.5, rely=0.90, relwidth=0.9, relheight=0.06, anchor='n')

		self.b1 = tk.Button(self.f12, text='上一页', bg='#ff6666', command=lambda : self.get_previousnews())
		self.b1.place(relx=0.35, rely=0, relwidth=0.1, relheight=1, anchor='nw')
		self.b2 = tk.Button(self.f12, text='下一页', bg='#ff6666', command=lambda : self.get_nextnews())
		self.b2.place(relx=0.55, rely=0, relwidth=0.1, relheight=1, anchor='nw')

		# 先执行一次获取信息函数，使打开子窗口时，首页头条信息
		self.get_nextnews()

	# 新闻格式(上一页)
	def format_news_previous(self, news_next):
		# try:
		# 换页条件
		if len(news_next['result']['data'])%3 != 0:
			if 0 < self.count <= len(news_next['result']['data']) - len(news_next['result']['data'])%3:
				self.count = self.count - 3
			else:
				self.count = len(news_next['result']['data']) - len(news_next['result']['data'])%3
		else:
			if 0 < self.count <= len(news_next['result']['data']) - 3:
				self.count = self.count - 3
			else:
				self.count = len(news_next['result']['data']) - 3


		# 返回三条信息
		title = ['', '', '']
		date = ['', '', '']
		url = ['', '', '']


		if len(news_next['result']['data']) % 3 == 0:
			for i_count in range(3):
				title[i_count] = news_next['result']['data'][self.count + i_count]['title']
				date[i_count] = news_next['result']['data'][self.count + i_count]['date']
				url[i_count] = news_next['result']['data'][self.count + i_count]['url']

		else:
			for i_count in range(len(news_next['result']['data']) % 3):
				title[i_count] = news_next['result']['data'][self.count + i_count]['title']
				date[i_count] = news_next['result']['data'][self.count + i_count]['date']
				url[i_count] = news_next['result']['data'][self.count + i_count]['url']

		# title一行达到27词，换行操作
		for i in range(3):
			if len(title[i]) >= 27:
				row_title = int(len(title[i]) / 25)
				list_title = list(title[i])
				for i_title in range(row_title):
					list_title.insert(25 + (25 + 1) * i_title, '\n          ')
				after_title = ''.join(list_title)
				after_title = str(after_title)
				title[i] = after_title

		# url一行达到50词，换行操作
		for j in range(3):
			if len(url[j]) >= 50:
				row_url = int(len(url[j]) / 50)
				list_url = list(url[j])
				for i_url in range(row_url):
					list_url.insert(50 + (50 + 1) * i_url, '\n          ')
				after_url = ''.join(list_url)
				after_url = str(after_url)
				url[j] = after_url

		# 输出新闻格式
		nextnews_str = ['', '', '']

		for i_out in range(3):
			if title[i_out] != '':
				nextnews_str[i_out] = '新闻标题：%s\n新闻时间：%s\n新闻链接：%s\n' % \
									  (title[i_out], date[i_out], url[i_out])

		# 前一条新闻与下一条新闻，换行间隔
		nextnews_out = "%s\n%s\n%s\n" % \
					   (nextnews_str[0], nextnews_str[1], nextnews_str[2])
		# except:
		# 		nextnews_str = 'There was a problem retrieving that information'

		return nextnews_out




	# 新闻格式(首页以及下一页)
	def format_news_next(self, news_next):
		# try:
		# 换页操作
		if len(news_next['result']['data'])%3 != 0:
			if self.count < len(news_next['result']['data']) - len(news_next['result']['data'])%3:
				self.count = self.count + 3
			else:
				self.count = 0
		else:
			if self.count < len(news_next['result']['data']) - 3:
				self.count = self.count + 3
			else:
				self.count = 0

		# 返回三条信息
		title = ['', '', '']
		date = ['', '', '']
		url = ['', '', '']


		if len(news_next['result']['data']) % 3 == 0 \
				or self.count < len(news_next['result']['data'])-len(news_next['result']['data'])%3:
			for i_count in range(3):
				title[i_count] = news_next['result']['data'][self.count + i_count]['title']
				date[i_count] = news_next['result']['data'][self.count + i_count]['date']
				url[i_count] = news_next['result']['data'][self.count + i_count]['url']

		elif len(news_next['result']['data']) % 3 != 0 \
				and self.count == len(news_next['result']['data'])-len(news_next['result']['data'])%3:
			for i_count in range(len(news_next['result']['data']) % 3):
				title[i_count] = news_next['result']['data'][self.count + i_count]['title']
				date[i_count] = news_next['result']['data'][self.count + i_count]['date']
				url[i_count] = news_next['result']['data'][self.count + i_count]['url']

		# title一行达到足够27词，换行操作
		for i in range(3):
			if len(title[i]) >= 27:
				row_title = int(len(title[i])/25)
				list_title = list(title[i])
				for i_title in range(row_title):
					list_title.insert(25 + (25 + 1) * i_title, '\n          ')
				after_title = ''.join(list_title)
				after_title = str(after_title)
				title[i] = after_title

		# title一行达到足够50词，换行操作
		for j in range(3):
			if len(url[j]) >= 50:
				row_url = int(len(url[j])/50)
				list_url = list(url[j])
				for i_url in range(row_url):
					list_url.insert(50 + (50 + 1) * i_url, '\n          ')
				after_url = ''.join(list_url)
				after_url = str(after_url)
				url[j] = after_url

		# 输出新闻格式
		nextnews_str = ['', '', '']

		for i_out in range(3):
			if title[i_out] != '':
				nextnews_str[i_out] = '新闻标题：%s\n新闻时间：%s\n新闻链接：%s\n' % \
							(title[i_out], date[i_out], url[i_out])
		# 前一条新闻与下一条新闻，换行间隔
		nextnews_out = "%s\n%s\n%s\n" %\
					   (nextnews_str[0], nextnews_str[1], nextnews_str[2])
	# except:
	# 		nextnews_str = 'There was a problem retrieving that information'

		return nextnews_out

	# 新闻类型选择(api特性)
	def select_news(self):
		type_list = ['top', 'shehui', 'guonei', 'guoji', 'yule',
					  'tiyu', 'junshi', 'keji', 'caijing', 'shishang']

		api_type = type_list[self.news_var.get()]

		return api_type

	# 新闻显示函数(上一页)
	def get_previousnews(self):
		url_news = 'http://v.juhe.cn/toutiao/index'
		params_news = {
			"type": self.select_news(),
			# 头条类型,top(头条，默认),shehui(社会),guonei(国内),guoji(国际),
			# yule(娱乐),tiyu(体育)junshi(军事),keji(科技),caijing(财经),shishang(时尚)

			"key": "ad0661ad78e54575445deeda852e3224",  # 申请的接口API接口请求Key
		}
		# 限制格式为utf-8
		querys_news = urllib.parse.urlencode(params_news).encode('utf-8')

		request_news = urllib.request.Request(url_news, data=querys_news)
		response_news = urllib.request.urlopen(request_news)
		content_news = response_news.read()
		if (content_news):
			try:
				result = json.loads(content_news)
				error_code = result['error_code']
				if (error_code == 0):
					# data = result['result']['data']
					self.L1['text'] = self.format_news_previous(result)
					# print(data)
				else:
					# print("请求失败:%s %s" % (result['error_code'], result['reason']))
					self.L1['text'] = "新闻请求失败:%s %s" % (result['error_code'], result['reason'])
			except Exception as e:
				self.L1['text'] = "新闻解析结果异常：%s" % e
				# print("解析结果异常：%s" % e)
		else:
			# 可能网络异常等问题，无法获取返回内容，请求异常
			# print("请求异常")
			self.L1['text'] = "新闻请求异常"


	# 新闻显示函数(首页和下一页)
	def get_nextnews(self):
		url_news = 'http://v.juhe.cn/toutiao/index'
		params_news = {
			"type": self.select_news(),
			# 头条类型,top(头条，默认),shehui(社会),guonei(国内),guoji(国际),
			# yule(娱乐),tiyu(体育)junshi(军事),keji(科技),caijing(财经),shishang(时尚)

			"key": "ad0661ad78e54575445deeda852e3224",  # 申请的接口API接口请求Key
		}
		# 限制格式为utf-8
		querys_news = urllib.parse.urlencode(params_news).encode('utf-8')

		request_news = urllib.request.Request(url_news, data=querys_news)
		response_news = urllib.request.urlopen(request_news)
		content_news = response_news.read()
		if (content_news):
			try:
				result = json.loads(content_news)
				error_code = result['error_code']
				if (error_code == 0):
					# data = result['result']['data']
					self.L1['text'] = self.format_news_next(result)
					# print(data)
				else:
					self.L1['text'] = "新闻请求失败:%s %s" % (result['error_code'], result['reason'])
					# print("请求失败:%s %s" % (result['error_code'], result['reason']))
			except Exception as e:
				self.L1['text'] = "新闻解析结果异常：%s" % e
				# print("解析结果异常：%s" % e)
		else:
			# 可能网络异常等问题，无法获取返回内容，请求异常
			# print("请求异常")
			self.L1['text'] = "新闻请求异常"

	# 测试函数(因为api每日有限制次数)
	def test(self):
		news_type = self.news_var.get()
		print(news_type)

# 测试函数
if __name__ == '__main__':
	window = tk.Tk()
	news = News(window)
	window.mainloop()
