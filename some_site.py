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


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # получаем файл из запроса
    file = request.files['image']
    if file is not None:
        # читаем изображение с помощью OpenCV
        img = Image.open(BytesIO(file.read()))

        # Resize the image with the new size
        fixed_width = 500
        width_percent = (fixed_width / float(img.size[0]))
        height_size = int((float(img.size[1]) * float(width_percent)))
        new_size = (fixed_width, height_size)
        img = img.resize(new_size)

        img.save(os.path.join(app.root_path, 'static', 'original.png'))
        return render_template('calculus.html', image_name='original.png')
    else:
        return "didn't open the file"


@app.route('/calculus', methods=['GET', 'POST'])
def calculus():
    if 'number-input' not in request.form:
        return "Number input field not found"

    # Get the value of the number input field
    angle = int(request.form['number-input'])

    # get the image
    img_path = os.path.join(app.root_path, 'static', 'original.png')
    img = Image.open(img_path)

    # Rotate the image
    rotated = img.rotate(angle)

    fixed_width = 500
    width_percent = (fixed_width / float(img.size[0]))
    height_size = int((float(img.size[1]) * float(width_percent)))

    # Resize the image with the new size
    new_size = (fixed_width, height_size)
    rotated = rotated.resize(new_size)

    # Save the rotated image with a new name
    answer_path = os.path.join(app.root_path, 'static', 'answer.png')
    rotated.save(answer_path)

    # Pass the name of the rotated image to the template
    return render_template('result.html', image_name='answer.png')


if __name__ == '__main__':
    app.run(debug=True)
