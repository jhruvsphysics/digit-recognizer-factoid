import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Input, Conv2D, Dense, Flatten, Dropout
from tensorflow.keras.models import Model

if __name__ == "__main__":
    # Get the data
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train, x_test = x_train/255.0, x_test/255.0

    # CNN expects 3D image samples: HxWxC
    x_train=np.expand_dims(x_train, -1)
    x_test=np.expand_dims(x_test, -1)
    np.shape(x_train), np.shape(x_test)

    # Need to figure out number of output nodes
    K = len(set(y_train))

    # Build the model (using Functional API)
    i = Input(shape=x_train[0].shape) #Input layer
    x = Conv2D(32, (3,3), strides=2, activation='relu')(i)
    x = Conv2D(64, (3,3), strides=2, activation='relu')(x)
    x = Conv2D(128, (3,3), strides=2, activation='relu')(x)
    x = Flatten()(x)
    x = Dropout(0.2)(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = Dense(K, activation='softmax')(x)

    model = Model(i, x)

    # Compile and fit
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    r = model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=100)

    model.save('see_digit.h5')