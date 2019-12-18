from flask import Flask
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_DIR = '/app/static/upload/'
DATA_DIR = '/app/static/data/'

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["WORKING_DIR"] = BASE_DIR + UPLOAD_DIR
app.config["DATA_DIR"] = BASE_DIR + DATA_DIR
app.config["ALLOWED_EXTENTIONS"] = ['png', 'jpg', 'jpeg', 'gif']
app.config["LOCAL_IMAGE"] = ""

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

from app import route
