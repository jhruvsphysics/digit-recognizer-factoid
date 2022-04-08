from flask import Flask, render_template, url_for, request, redirect
from smooth_brain_digit_recognizer import smooth_brain_predict
from guess_digit import guess_digit

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = processb64(request.data)
        np.save('image.npy', image)
        # smooth_brain_predict(image)
        guess, confidence = guess_digit(image)
        print('I guess.... ', guess)
        print('with confidence ', confidence)
        
        return f"{guess} {confidence}"
    else:
        return render_template('index.html')

@app.route('/smooth-brain', methods=['POST'])
def smooth_brain():
    if request.method == 'POST':
        image = processb64(request.data)
        np.save('image.npy', image)
        guess, confidence = smooth_brain_predict(image)
        print('I guess.... ', guess)
        print('with confidence ', confidence)
        
        return f"{guess} {confidence}"

from PIL import Image, ImageOps
import base64
import io
import numpy as np

def processb64(data):
    print(data)
    # decode base64 to bytes
    base64_decoded = base64.b64decode(data)

    # convert to BytesIO, and open via Image.open
    image = Image.open(io.BytesIO(base64_decoded))
    # resize
    image = image.resize((28, 28))
    # convert to grayscale image
    gray_image = ImageOps.grayscale(image)
    image_np = np.array(gray_image)
    return image_np


if __name__ == "__main__":
    app.run(debug=True)