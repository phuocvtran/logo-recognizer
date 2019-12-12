from app import app
from flask import flash, Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from app.nbnn import NaiveBayesNN
import cv2
import os
import h5py
import time


LIST_IMG = []
IMG_PATH = app.config["WORKING_DIR"]
DATA_DIR = app.config["DATA_DIR"]


model = NaiveBayesNN()
hf = h5py.File(DATA_DIR + "dsift_81.h5", "r")
model.fit(hf)


def allowed_file(filename):
    if not '.' in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.lower() in app.config["ALLOWED_EXTENTIONS"]:
        return True
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if request.form['button'] == 'Upload':
            if request.files:
                file = request.files['image']
                if file.filename == '':
                    print("No file name")
                    print(request.form['button'])
                    return redirect(request.url)
                if not allowed_file(file.filename):
                    print("That image is not allowed")
                    return redirect(request.url)
                else:
                    filename = secure_filename(file.filename)
                    app.config["LOCAL_IMAGE"] = filename
                    file.save(os.path.join(
                        app.config["WORKING_DIR"], filename))
                    return render_template('home.html', filename=filename)

            else:
                flash('No file part')
                return redirect(request.url)
        elif request.form['button'] == 'Predict':
            filename = app.config["LOCAL_IMAGE"]
            path = IMG_PATH + filename
            img = cv2.imread(path)
            LIST_IMG.append(img)
            print(LIST_IMG)
            start = time.time()
            label = model.predict(LIST_IMG, step=10)
            end = time.time()
            total = end - start
            LIST_IMG.clear()
            hf.close()
            return render_template('home.html', filename=filename, label=label[len(label) - 1], total=round(total, 2))
    return render_template('home.html')
