import tkinter as tk
import urllib,  json
import requests
import urllib.request
import urllib.parse
import urllib.error

class Weather:
	def __init__(self,window):
		self.window = window
		self.window = tk.Toplevel(self.window)
		self.window.title('天气')
		self.canvas = tk.Canvas(self.window, height=500, width=600)
		self.canvas.pack()
		self.f1 = tk.Frame(self.window, bg='#80c1ff', bd=5)
		self.f1.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

		self.e1 = tk.Entry(self.f1, font=40)
		self.e1.place(relwidth=0.6, relheight=1)

		self.b1 = tk.Button(self.f1, text="查询", font=40, command=lambda: self.get_weather(self.e1.get()))
		self.b1.place(relx=0.65, relheight=1, relwidth=0.35)

		self.f2 = tk.Frame(self.window, bg='#80c1ff', bd=10)
		self.f2.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

		self.L1 = tk.Label(self.f2, font=60, bd=5, justify='left')
		self.L1.place(relwidth=1, relheight=1, anchor='nw')
		self.get_init_weather(self.get_weather_city())

	# 获取IP所在城市
	def get_weather_city(self):
		url_ip = 'http://ifconfig.me/ip'
		ip = requests.get(url_ip, timeout=1).text.strip()

		url_address = 'http://apis.juhe.cn/ip/ipNew'
		params_address = {
			"ip": ip,  # 查询的IP地址
			"key": "9d0e99638124a2d47eab699d98b7fdb3",  # 申请的接口API接口请求Key
		}
		querys_address = urllib.parse.urlencode(params_address).encode('utf-8')
		request_address = urllib.request.Request(url_address, data=querys_address)
		response_address = urllib.request.urlopen(request_address)
		content_address = response_address.read()
		if (content_address):
			try:
				result = json.loads(content_address)
				# print(result)
				error_code = result['error_code']
				if (error_code == 0):
					city = result['result']['City']
					print('城市：%s\n' % (city))
				else:
					self.L1['text'] = 'IP归属地请求失败，无法查询该城市\n'
					# print("IP归属地请求失败:%s %s" % (result['error_code'], result['reason']))
			except Exception as e:
				self.L1['text'] = 'IP归属地解析结果异常\n'
				# print("解析结果异常：%s" % e)
		else:
			# 可能网络异常等问题，无法获取返回内容，请求异常
			self.L1['text'] = 'IP归属地请求异常\n'
			# print("请求异常")
		return city


	# 查询某城市的天气
	def get_weather(self,city):
		api_url = 'http://apis.juhe.cn/simpleWeather/query'
		# if city == '':
		# 	self.L1['text'] = '输入不能为空'
		params_weather_dict = {
			"city": city,  # 查询天气的城市名称，如：北京、苏州、上海
			"key": "4b41866c4023f4e84a96c37bd844b384",  # 申请的接口API接口请求Key
		}
		params_weather = urllib.parse.urlencode(params_weather_dict)
		try:
			req_weather = urllib.request.Request(api_url, params_weather.encode())
			response_weather = urllib.request.urlopen(req_weather)
			content_weather = response_weather.read()
			if content_weather:
				try:
					result = json.loads(content_weather)
					error_code = result['error_code']
					if (error_code == 0):
						temperature = result['result']['realtime']['temperature']
						humidity = result['result']['realtime']['humidity']
						info = result['result']['realtime']['info']
						wid = result['result']['realtime']['wid']
						direct = result['result']['realtime']['direct']
						power = result['result']['realtime']['power']
						aqi = result['result']['realtime']['aqi']
						# print("温度：%s\n湿度：%s\n天气：%s\n天气标识：%s\n风向：%s\n风力：%s\n空气质量：%s" % (
						# 	temperature, humidity, info, wid, direct, power, aqi))
						self.L1['text'] = "温度：%s\n湿度：%s\n天气：%s\n天气标识：%s\n风向：%s\n风力：%s\n空气质量：%s" % (
							temperature, humidity, info, wid, direct, power, aqi)
					else:
						# print("请求失败:%s %s" % (result['error_code'], result['reason']))
						self.L1['text'] = "天气请求失败:\n错误代码为:%s\n错误原因为:%s\n" % (result['error_code'], result['reason'])
				except Exception as e:
					self.L1['text'] = "天气解析结果异常：%s\n" % e
					# print("解析结果异常：%s" % e)
			else:
				# 可能网络异常等问题，无法获取返回内容，请求异常
				# print("请求异常")
				self.L1['text'] = "天气请求异常"
		except urllib.error.HTTPError as err:
			# print(err)
			self.L1['text'] = "天气url请求失败：%s\n" % err
		except urllib.error.URLError as err:
			# 其他异常
			# print(err)
			self.L1['text'] = "天气url请求失败：%s\n" % err



	# 用当前城市数据初始化信息框
	def get_init_weather(self, city):
		api_url = 'http://apis.juhe.cn/simpleWeather/query'
		if city == '' :
			city = '广州'
		params_weather_dict = {
			"city": city,  # 查询天气的城市名称，如：北京、苏州、上海
			"key": "4b41866c4023f4e84a96c37bd844b384",  # 申请的接口API接口请求Key
		}
		params_weather = urllib.parse.urlencode(params_weather_dict)
		try:
			req_weather = urllib.request.Request(api_url, params_weather.encode())
			response_weather = urllib.request.urlopen(req_weather)
			content_weather = response_weather.read()
			if content_weather:
				try:
					result = json.loads(content_weather)
					error_code = result['error_code']
					if (error_code == 0):
						temperature = result['result']['realtime']['temperature']
						humidity = result['result']['realtime']['humidity']
						info = result['result']['realtime']['info']
						wid = result['result']['realtime']['wid']
						direct = result['result']['realtime']['direct']
						power = result['result']['realtime']['power']
						aqi = result['result']['realtime']['aqi']
						# print("温度：%s\n湿度：%s\n天气：%s\n天气标识：%s\n风向：%s\n风力：%s\n空气质量：%s" % (
							# temperature, humidity, info, wid, direct, power, aqi))
						self.L1['text'] = "温度：%s\n湿度：%s\n天气：%s\n天气标识：%s\n风向：%s\n风力：%s\n空气质量：%s" % (
							temperature, humidity, info, wid, direct, power, aqi)
					else:
						# print("请求失败:%s %s" % (result['error_code'], result['reason']))
						self.L1['text'] = "天气请求失败:\n错误代码为:%s\n错误原因为:%s\n" % (result['error_code'], result['reason'])
				except Exception as e:
					# print("解析结果异常：%s" % e)
					self.L1['text'] = "天气解析结果异常：%s\n" % e
			else:
				# 可能网络异常等问题，无法获取返回内容，请求异常
				self.L1['text'] = "天气请求异常\n"
				# print("请求异常")
		except urllib.error.HTTPError as err:
			self.L1['text'] = "天气url异常：%s\n" % err
			# print(err)
		except urllib.error.URLError as err:
			self.L1['text'] = "天气url异常：%s\n" % err
			# 其他异常
			# print(err)

# 测试函数
if __name__ == '__main__':
	window = tk.Tk()
	weather = Weather(window)
	window.mainloop()