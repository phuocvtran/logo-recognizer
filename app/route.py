from app import app
from flask import flash, Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from app.nbnn import NaiveBayesNN
from app.haarcascade import HaarCascade
import cv2
import os
import h5py
import time

LIST_IMG = []
IMG_PATH = app.config["WORKING_DIR"]
DATA_DIR = app.config["DATA_DIR"]

model = NaiveBayesNN()
keys = model.fit(DATA_DIR + "dsift.h5")
cascade = HaarCascade()
cascade.fit("app/static/data/haar", ["adidas", "aldi", "apple", "bmw", "cocacola", "pepsi"]) # hiện tại chỉ có 2 keys sau sẽ sửa lại
i = 0

def allowed_file(filename):
    if '.' not in filename:
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
                    return redirect(request.url)
                if not allowed_file(file.filename):
                    return redirect(request.url)
                else:
                    filename = secure_filename(file.filename)
                    app.config["LOCAL_IMAGE"] = filename
                    file.save(os.path.join(
                        IMG_PATH, filename))
                    return render_template('home.html', filename=filename)

            else:
                flash('No file part')
                return redirect(request.url)
        elif request.form['button'] == 'Predict':
            filename = app.config["LOCAL_IMAGE"]
            path = IMG_PATH + filename
            LIST_IMG = cascade.detectAndCrop(path, "app/static/upload/detect_img.jpg")
            filename = "detect_img.jpg"
            start = time.time()
            labels = model.predict(LIST_IMG, step=10)
            end = time.time()
            total = end - start
            LIST_IMG.clear()

            if not labels:
                return render_template('home.html', nolabel=filename)

            string = []
            i = 1
            for label in labels:
                string.append(str(i) + ". " + str(label))
                i += 1

            return render_template('home.html', filename=filename, labels=string, total=round(total, 2))
    return render_template('home.html')


@app.route('/model', methods=['GET', 'POST'])
def upload_image_with_id():
    if request.method == 'POST':
        if request.form['button'] == 'Upload':
            if request.files:
                file = request.files['image']
                if file.filename == '':
                    return redirect(request.url)
                if not allowed_file(file.filename):
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
            start = time.time()
            label = model.predict(LIST_IMG, step=10)
            end = time.time()
            total = end - start
            LIST_IMG.clear()
            return render_template('home.html', filename=filename, labels=label, total=round(total, 2))
    return render_template('home.html')
