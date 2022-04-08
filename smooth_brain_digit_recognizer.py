#multi-class logistic regression: 1-hidden layer feedforward neural network
from tensorflow.keras.datasets import mnist
import numpy as np
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

def smooth_brain_predict(x):
  # load parameters
  W = np.load('W.npy')
  b = np.load('b.npy')
  mu, std = np.load('mu_std.npy')

  # preprocess and normalize
  x = x.reshape(1,28*28)
  x = (x-mu)/std
  print(x)

  # predict
  # a = x.dot(W) + b
  P_y = forward(x, W, b)
  y = np.argmax(P_y, axis=1)
  return [P_y, y]

# helper functions
def flatten(X):
  # This will flatten the last two indices
  # if [[a, b], [c, d]] -> [a, b, c, d] per sample
  N, dim1, dim2 = X.shape
  return X.reshape(N, dim1*dim2)

def onehot(Y):
  K = np.max(Y)+1
  return np.eye(K)[Y]

def softmax(a):
  expA = np.exp(a)
  return expA/np.sum(expA, axis=1, keepdims=True)

def forward(X, W, b):
  return softmax(X.dot(W) + b)

def predict(P_Y):
  return np.argmax(P_Y, axis=1)

def cross_entropy(T, Y):
  return -np.mean(np.log(Y)[np.arange(len(T)), np.argmax(T, axis=1)])

def classification_rate(Y, P):
  return np.mean(Y == P)


# For training. Only need to run once.
def train(epochs):
  (Xtrain, Ytrain), (Xtest, Ytest) = mnist.load_data()

  Xtrain, Ytrain = shuffle(Xtrain, Ytrain)
  Xtest, Ytest = shuffle(Xtest, Ytest)

  print('size of Xtrain:', Xtrain.shape)
  print('size of Ytrain:', Ytrain.shape)
  print('size of Xtest:', Xtest.shape)
  print('size of Ytest:', Ytest.shape)

  Ytest_ind = onehot(Ytest)
  Ytrain_ind = onehot(Ytrain)

  Xtest = flatten(Xtest)
  Xtrain = flatten(Xtrain)

  # normalize the data
  mu = Xtrain.mean(axis=0)
  std = Xtrain.std(axis=0)

  idx = np.where(std == 0)[0]
  assert(np.all(std[idx] == 0))

  np.place(std, std==0, 1)

  Xtrain = (Xtrain-mu)/std
  Xtest = (Xtest-mu)/std

  N, D = Xtrain.shape
  K = len(Ytrain_ind[0])
  Ntest = len(Ytest)



  # Initialize weights
  W = np.random.randn(D, K)/np.sqrt(D)
  b = np.zeros(K)

  # Training Algorithm
  train_costs = []
  test_costs = []
  train_errors = []
  test_errors = []
  learning_rate = 0.00001

  for i in range(epochs):
    P_Y = forward(Xtrain, W, b)
    P_Ytest = forward(Xtest, W, b)
    c = cross_entropy(Ytrain_ind, P_Y)
    ctest = cross_entropy(Ytest_ind, P_Ytest)
    err = 1-classification_rate(Ytrain, predict(P_Y))
    err_test = 1-classification_rate(Ytest, predict(P_Ytest))

    train_costs.append(c)
    test_costs.append(ctest)
    train_errors.append(err)
    test_errors.append(err_test)

    if i%250==0:
      print('train cost:', c)
      print('test cost:', ctest)
      print('train error', err)
      print('test error', err_test)
      print('at step:', i)

    # gradient descent
    d_WJ = Xtrain.T.dot(P_Y - Ytrain_ind)
    d_bJ = np.sum(P_Y - Ytrain_ind, axis=0)
    W -= learning_rate*d_WJ
    b -= learning_rate*d_bJ

  fig, ax = plt.subplots()  
  ax.plot(train_costs, label="train costs")
  ax.plot(test_costs, label="test costs")
  ax.legend(['train costs', 'test costs'])
  ax.set_title("Train and Test Costs")
  ax.set_ylabel("costs")
  ax.set_xlabel("epochs")
  fig.savefig('costs.png')

  fig, ax = plt.subplots()  
  ax.plot(train_errors, label="train errors")
  ax.plot(test_errors, label="test errors")
  ax.legend(['train errors', 'test errors'])
  ax.set_title("Train and Test Classification Errors")
  ax.set_ylabel("error rate")
  ax.set_xlabel("epochs")
  fig.savefig('errors.png')

  # Save the weights and bias
  np.save('W.npy', W)
  np.save('b.npy', b)
  np.save('mu_std.npy', np.array([mu, std]))

  

if __name__=="__main__":
  train(2500)



