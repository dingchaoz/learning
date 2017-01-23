## Run this in ipython: %run test.py

import numpy as np

num_train = 50
num_class = 10
input_size = 300
hidden_size = 100
output_size = num_class
std=1e-4


X = np.random.randn(num_train,input_size)
y = np.random.randint(0,9,(num_train))


W1 = std * np.random.randn(input_size, hidden_size)
b1 = np.zeros(hidden_size)
W2 = std * np.random.randn(hidden_size, output_size)
b2 = np.zeros(output_size)


 # Compute the forward pass
 scores = None
 H1 = X.dot(W1) + b1
 relu1 = np.maximum(H1, np.zeros_like(H1))
 # scores = W2.T.dot(relu1.T).T + b2
 scores = relu1.dot(W2) + b2


