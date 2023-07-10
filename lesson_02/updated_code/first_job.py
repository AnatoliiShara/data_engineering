import os
import requests
from flask import Flask, request
import json

app = Flask(__name__)

os.environ['AUTH_TOKEN'] = '2b8d97ce57d401abd89f45b0079d8790edd940e6'
RAW_DIR = '/home/sharaa/Documents/data_engineering/lesson2/updated_code/raw/sales/2022-08-09'

def extract_sales_data(date, page):
    response = requests.get(
        url='https://fake-api-vycpfa6oca-uc.a.run.app/sales',
        params={'date': date, 'page': page},
        headers={'Authorization': AUTH_TOKEN},
    )
    if response.status_code == 200:
        return response.json()
    else:
        return None

def save_sales_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)

@app.route('/', methods=['POST'])
def process_request():
    request_data = request.get_json()
    date = request_data['date']
    raw_dir = request_data['raw_dir']
    raw_dir = raw_dir.replace('RAW_DIR', RAW_DIR)
    os.makedirs(raw_dir, exist_ok=True)
    
    for page in range(1, 6):  # Assuming there are 5 pages of data
        sales_data = extract_sales_data(date, page)
        if sales_data:
            file_name = f"sales_{date}_{page}.json"
            file_path = os.path.join(raw_dir, file_name)
            save_sales_data(sales_data, file_path)
    
    return 'Data extraction and saving completed successfully!'

if __name__ == '__main__':
    app.run(port=8081)
