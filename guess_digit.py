import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

def guess_digit(image):
    model = tf.keras.models.load_model('see_digit.h5')
    image = image/255.0
    image=np.expand_dims(image, 2)
    image=np.expand_dims(image, 0)
    P = model.predict(image)
    return [P.argmax(), P.max()]