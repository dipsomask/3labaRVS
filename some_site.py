import os
from io import BytesIO

from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import cv2
from PIL import Image

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    # получаем файл из запроса
    file = request.files['image']
    if file is not None:
        pass
    else:
        return "didn't open the file"
    # читаем изображение с помощью OpenCV
    img = Image.open(BytesIO(file.read()))
    img.save(os.path.join(app.root_path, 'static', 'original.png'))
    return redirect(url_for('calculus'))


@app.route('/calculus', methods=['POST'])
def calculus():
    # Get the value of the number input field
    angle = int(request.form['number-input'])
    # Load the image
    img_path = os.path.join(app.root_path, 'static', 'original.png')
    img = Image.open(img_path)
    # Rotate the image
    rotated = img.rotate(angle)
    #(h, w) = img.shape[:2]
    #center = (w / 2, h / 2)
    rotated.save(os.path.join(app.root_path, 'static', 'answer.png'))
    #m = cv2.getRotationMatrix2D(center, angle, 1.0)
    #rotated = cv2.warpAffine(img, m, (w, h))
    #cv2.imwrite('static/rotated.jpg', rotated)
    return redirect(url_for('results'))


@app.route('/results')
def results():
    photo_url = url_for('static', filename='rotated.png')
    return render_template('result.html', photo_url=photo_url)


if __name__ == '__main__':
    app.run(debug=True)
