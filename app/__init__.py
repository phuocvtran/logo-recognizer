from flask import Flask
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_DIR = '/app/static/upload/'
DATA_DIR = '/app/static/data/'

app.config["WORKING_DIR"] = BASE_DIR + UPLOAD_DIR
app.config["DATA_DIR"] = BASE_DIR + DATA_DIR
app.config["ALLOWED_EXTENTIONS"] = ['png', 'jpg', 'jpeg', 'gif']
app.config["LOCAL_IMAGE"] = ""

from app import route
