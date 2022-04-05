from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = processb64(request.data)
        print(image.shape)
        return "success"
    else:
        return render_template('index.html')

from PIL import Image, ImageOps
import base64
import io
import numpy as np

def processb64(data):
    print(data)
    # decode base64 to bytes
    base64_decoded = base64.b64decode(data)
    print(type(base64_decoded))
    print(base64_decoded)
    print(type("cccc"))
    print('=====================================')
    print(io.BytesIO(base64_decoded))

    # convert to BytesIO, and open via Image.open
    image = Image.open(io.BytesIO(base64_decoded))
    image = image.resize((28, 28))
    # convert to grayscale image
    gray_image = ImageOps.grayscale(image)
    image_np = np.array(gray_image)
    return image_np


if __name__ == "__main__":
    app.run(debug=True)