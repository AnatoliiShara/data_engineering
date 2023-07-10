import os
import json
import fastavro
from flask import Flask, request

app = Flask(__name__)

RAW_DIR = '/home/sharaa/Documents/data_engineering/lesson2/updated_code/raw/sales/2022-08-09'
STG_DIR = '/home/sharaa/Documents/data_engineering/lesson2/updated_code/stg/sales/2022-08-09'

def convert_json_to_avro(file_path, output_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    
    with open(output_path, 'wb') as avro_file:
        fastavro.writer(avro_file, data, schema=json_file.schema)

@app.route('/', methods=['POST'])
def process_request():
    request_data = request.get_json()
    raw_dir = request_data['raw_dir'].replace('RAW_DIR', RAW_DIR)
    stg_dir = request_data['stg_dir'].replace('RAW_DIR', STG_DIR)
    os.makedirs(stg_dir, exist_ok=True)
    
    for filename in os.listdir(raw_dir):
        if filename.endswith('.json'):
            raw_file_path = os.path.join(raw_dir, filename)
            stg_file_name = filename.replace('.json', '.avro')
            stg_file_path = os.path.join(stg_dir, stg_file_name)
            convert_json_to_avro(raw_file_path, stg_file_path)
    
    return 'Conversion from JSON to Avro completed successfully!'

if __name__ == '__main__':
    app.run(port=8082)