import os
from io import BytesIO

from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import pandas as pd
from PIL import Image
from captcha.image import ImageCaptcha

app = Flask(__name__)


# generate a random string for the captcha
def generate_captcha_text(length=5):
    captcha_text = 'skjdhgkjsdhgk'
    for i in range(length):
        import random
        captcha_text += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return captcha_text


# create the captcha image and return the HTML code
def create_captcha():
    captcha_text = generate_captcha_text()
    image = ImageCaptcha().generate(captcha_text)
    image_data = image.getvalue()
    html = '<img src="data:image/png;base64,' + str(image_data, 'utf-8') + '">'
    html += '<input type="text" name="captcha">'
    return captcha_text, html


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

    # Load the image
    img_path = os.path.join(app.root_path, 'static', 'original.png')
    img = Image.open(img_path)

    # Convert the image to a Pandas DataFrame
    df = pd.DataFrame(list(img.getdata()), columns=['Red', 'Green', 'Blue'])

    # Create histograms for each color channel
    histograms = df.apply(pd.Series.value_counts, bins=256)

    # Rename the columns of the histograms DataFrame
    histograms.columns = ['Red', 'Green', 'Blue']

    # Concatenate the histograms into a single DataFrame
    color_distribution = pd.concat([histograms], axis=0)

    # Update the layout of the DataFrame
    color_distribution.index.name = 'Color Value'
    color_distribution.columns.name = 'Color Channel'

    # Save the color distribution plot as a PNG image
    color_distribution.plot(kind='bar', stacked=True, figsize=(5, 5)).get_figure().savefig('static/firstgraf.png')
    imggraph_path = os.path.join(app.root_path, 'static', 'firstgraf.png')
    imggraph = Image.open(imggraph_path)
    resizeimg(imggraph)
    imggraph.save(imggraph_path)

    # Rotate the image
    rotated = img.rotate(angle)
    resizeimg(rotated)

    # Save the rotated image with a new name
    answer_path = os.path.join(app.root_path, 'static', 'answer.png')
    rotated.save(answer_path)

    # Convert the image to a Pandas DataFrame
    df = pd.DataFrame(list(rotated.getdata()), columns=['Red', 'Green', 'Blue'])

    # Create histograms for each color channel
    histograms = df.apply(pd.Series.value_counts, bins=256)

    # Rename the columns of the histograms DataFrame
    histograms.columns = ['Red', 'Green', 'Blue']

    # Concatenate the histograms into a single DataFrame
    color_distribution = pd.concat([histograms], axis=0)

    # Update the layout of the DataFrame
    color_distribution.index.name = 'Color Value'
    color_distribution.columns.name = 'Color Channel'

    # Save the color distribution plot as a PNG image
    color_distribution.plot(kind='bar', stacked=True, figsize=(5, 5)).get_figure().savefig('static/secondgraph.png')
    imggraph_path = os.path.join(app.root_path, 'static', 'secondgraph.png')
    imggraph = Image.open(imggraph_path)
    resizeimg(imggraph)
    imggraph.save(imggraph_path)

    # Pass the name of the rotated image to the template
    return render_template('result.html', image_name='answer.png', image_name2='firstgraf.png',
                           image_name3='secondgraph.png', image_mame4='original.png')


def resizeimg(img):
    fixed_width = 500
    width_percent = (fixed_width / float(img.size[0]))
    height_size = int((float(img.size[1]) * float(width_percent)))

    # Resize the image with the new size
    new_size = (fixed_width, height_size)
    img = img.resize(new_size)
    return img


if __name__ == '__main__':
    app.run(debug=True)
