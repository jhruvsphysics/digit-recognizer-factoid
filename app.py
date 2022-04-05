from flask import Flask, render_template, url_for, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = processb64(request.data)
        print(image)
        print(image.shape)
        return "success"
    else:
        return render_template('index.html')

from PIL import Image
import base64
import io
import numpy as np
import torch

def processb64(data):
    print(data)
    base64_decoded = base64.b64decode(data)
    print(type(base64_decoded))
    print(base64_decoded)
    print(type("cccc"))
    print('=====================================')
    print(io.BytesIO(base64_decoded))
    # image = Image.Image.frombytes(1, base64_decoded)
    image = Image.open(io.BytesIO(base64_decoded))
    image_np = np.array(image)
    return image_np

# def processb64(data):
#     print(data)
#     base64_decoded = base64.b64decode(data)
#     print(base64_decoded)
#     # image = Image.open(io.BytesIO(base64_decoded)
#     print(image)
#     return true
#     # image_np = np.array(image)
#     # image_torch = torch.tensor(np.array(image))
#     # return image_np


if __name__ == "__main__":
    app.run(debug=True)