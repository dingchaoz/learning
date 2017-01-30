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

#############################################################################
    # Compute the backward pass, computing the derivatives of the weights #
    # and biases. Store the results in the grads dictionary. For example,       #
    # grads['W1'] should store the gradient on W1, and be a matrix of same size #
 #############################################################################

 # Compute the forward pass
scores = None
H1 = X.dot(W1) + b1
relu1 = np.maximum(H1, np.zeros_like(H1))
# scores = W2.T.dot(relu1.T).T + b2
scores = relu1.dot(W2) + b2


# Compute loss, own method
correct_class_score = scores[range(len(y)),y]
correct_class_score_exp = np.exp(correct_class_score)
scores_exp = np.exp(scores)
sum_exp_classes = np.sum(scores_exp, axis = 1)
softmax = correct_class_score_exp/ sum_exp_classes
sum_loss = -np.log(softmax)
softmax_loss = np.mean(sum_loss)
regularization = 0.5 * (np.sum(W1 * W1) + np.sum(W2 * W2))
 # regularization = 0.5 * reg * np.sum(W * W)
loss = softmax_loss + regularization

# The other method, produces the same result
# log_c = -np.max(scores, axis=1)
# exp_scores = np.exp((scores.T + log_c).T)
# exp_correct_class = exp_scores[range(len(y)),y]
# sum_exp_classes = np.sum(exp_scores, axis = 1)
# softmax = exp_correct_class / sum_exp_classes
# sum_loss = -np.log(softmax)
# softmax_loss = np.mean(sum_loss)
# regularization = 0.5 * reg * (np.sum(W1 * W1) + np.sum(W2 * W2))
#  # regularization = 0.5 * reg * np.sum(W * W)
# loss = softmax_loss + regularization