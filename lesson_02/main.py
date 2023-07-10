import os
import requests
import json
from flask import Flask, request

app = Flask(__name__)

# this line sets the value of "AUTH_Token" env variable to provided token. 
# env variables are used to store configuration values
os.environ['AUTH_TOKEN'] = '2b8d97ce57d401abd89f45b0079d8790edd940e6'

# this line assigns the base directory path where 'raw' directory will be created. 
# It specifies the location where JSON-files will be stores
base_dir = '/home/sharaa/Documents/data_engineering/lesson2'

#this line joins the base directory and 'raw' directory to create full path to 'raw' directory
raw_dir = os.path.join(base_dir, 'raw')

# this is a decorator in Flask that specifies the route for the root URL('/').
# It indicates that the following function will be called when a POST request is received at that URL
@app.route('/', methods=['POST'])
def save_sales_data():
    """This is tha function that handles POST request to the root URL.
        It's executed when a POST request is received and it performs the necessary operations to save sales data
    """
    # this line retrieves JSON data from the requested payload. 
    # It uses "request" object from Flask to access JSON data sent with POST request
    data = request.json
    # this line extracts the value of "date" from JSON data. 
    # It assumes that JSON data contains 'date' field and it assigns to "date" variable
    date = data['date']
    # this line extracts value of 'raw_dir' field form JSON
    raw_dir_param = data['raw_dir']
    
    # Create the raw directory if it doesn't exist
    # This line creates full path to dynamic raw directory by joining base raw directory path 'raw_dir'
    # and value of 'raw_dir_param' extracted from JSON data. It uses 'os.path.join()' to concatenate paths
    dynamic_raw_dir = os.path.join(raw_dir, raw_dir_param)
    # with 'exist_ok' argument ensures that directory is created even if it already exists
    os.makedirs(dynamic_raw_dir, exist_ok=True)
    
    # Clear the contents of the raw directory before writing new files
    # this line retrieves a list of files names present in the dynamic raw directory.
    # it uses 'listdir' to list all the files in the directory 
    file_list = os.listdir(dynamic_raw_dir)
    # this loop iterates over each file in 'filelist'
    for file_name in file_list:
        # This line creates full path to a file by joining dynamic raw directory path and current file name.
        # it uses 'os.path.join' to concatenate paths
        file_path = os.path.join(dynamic_raw_dir, file_name)
        # this line removes file specified by 'file_path'. It deletes file from the system
        os.remove(file_path)
    
    # This line sets up headers for HTTP request. It creates a dict with "Authorisation" header, 
    # using value of 'AUTH_TOKEN' environment variable as token
    headers = {'Authorization': os.environ.get('AUTH_TOKEN')}
    page = 1
    while True:
        # ends a GET request to the specified URL with the provided parameters (date and page) and headers.
        response = requests.get(
            url='https://fake-api-vycpfa6oca-uc.a.run.app/sales',
            params={'date': date, 'page': page},
            headers=headers
        )
        # hecks if the response status code is not 200 (OK). If it's not, the loop is exited.
        if response.status_code != 200:
            break
        
        # Save data from the API in separate JSON files
        # This line constructs the file name for the JSON file based on the date and page number. 
        # It uses an f-string to dynamically insert the values into the string.
        file_name = f"sales_{date}_{page}.json"
        #  This line creates the full path to the JSON file by joining the dynamic raw directory path and the file name. 
        # It uses os.path.join() to concatenate the paths.
        file_path = os.path.join(dynamic_raw_dir, file_name)
        # This line opens the file specified by file_path in write mode. 
        # It uses a with statement to ensure that the file is properly closed after writing.
        with open(file_path, 'w') as file:
            # This line writes the JSON data from the API response to the file. 
            # It uses json.dumps() to serialize the JSON data to a string representation, and then writes the string to the file.
            file.write(json.dumps(response.json()))
        #  This line increments the page number for the next iteration of the loop. 
        # It increases the value of the page variable by 1.
        page += 1
    #  This line returns a string indicating that the sales data has been successfully saved in the 'raw' directory. 
    # This is the response sent back to the client making the POST request.
    return "Sales data saved in the 'raw' directory."

# This line checks if the script is being executed directly (not imported as a module).
if __name__ == '__main__':
    # This line starts the Flask application and runs the web server on port 8081 in debug mode. 
    # It listens for incoming requests and handles them accordingly.
    app.run(port=8081, debug=True)