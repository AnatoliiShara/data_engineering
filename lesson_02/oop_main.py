import os 
import requests
import json
from flask import Flask, request

class SalesDataSaver:

	def __init__(self):
		self.app = Flask(__name__)
		self.app.route('/', methods=['POST'])(self.save_sales_data)
		self.base_dir = '/home/sharaa/Documents/data_engineering/lesson2'
		self.raw_dir = os.path.join(self.base_dir, 'raw')
		os.environ['AUTH_TOKEN'] = '2b8d97ce57d401abd89f45b0079d8790edd940e6'

	def run(self):
		self.app.run(port=8081, debug=True)

	def save_sales_data(self):
		data = request.json
		date = data['date']
		raw_dir_param = data['raw_dir']
		
		# create raw directory if it doesn't exist
		dynamic_raw_dir = os.path.join(self.raw_dir, raw_dir_param)
		os.makedirs(dynamic_raw_dir, exist_ok=True)

		# clear contents of raw directory before writing new files
		file_list = os.listdir(dynamic_raw_dir)
		for file_name in file_list:
			file_path = os.path.join(dynamic_raw_dir, file_name)
			os.remove(file_path)

		headers = {'Authorization': os.environ.get('AUTH_TOKEN')}
		page = 1
		while True:
			response = requests.get(
				url='https://fake-api-vycpfa6oca-uc.a.run.app/sales',
				params={'date': date, 'page': page},
				headers=headers
				)
			if response.status_code != 200:
				break

		# save data from API in separate JSON files
		file_name = f"sales_{date}_{page}.json"
		file_path = os.path.join(dynamic_raw_dir, file_name)
		with open(file_path, 'w') as file:
			file.write(json.dumps(response.json()))

		page += 1
		return "Sales data saved in 'raw' directory"

if __name__ == "__main__":
	data_saver = SalesDataSaver()
	data_saver.run()

