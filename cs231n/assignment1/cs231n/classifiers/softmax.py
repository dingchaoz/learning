import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)
  num_train = X.shape[0]
  num_class = dW.shape[1]

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  # https://github.com/dingchaoz/CS231/blob/master/assignment1/cs231n/classifiers/softmax.py
  # look into the one above for inspiration, the W,X shape are different though
  # http://math.stackexchange.com/questions/945871/derivative-of-softmax-loss-function
  # also look into the above discussion to make sure you got the softmax gradient worked right
  loss = 0.0
  for i in xrange(num_train):
    # Get score of all class for the image
    scores = X[i].dot(W)

    # Subtract the max score for stability
    scores -= np.max(scores)


    # Get the exp scores
    exp_scores = np.exp(scores)/np.sum(np.exp(scores))

    # Get the softmax score which is the correct class normalized exp score
    softmax_score = exp_scores[y[i]]

    # Compute loss
    loss += -np.log(softmax_score)

    # Compute gradient
    # http://eli.thegreenplace.net/2016/the-softmax-function-and-its-derivative/

    for j in xrange(num_class):
      if j == y[i]:
        dW[:,j] += -X[i].T + exp_scores[j] * X[i].T
      else:
        dW[:,j] += X[i].T * exp_scores[j]


  # Right now the loss is a Wsum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  # Same with gradient
  dW /= num_train

  # Add regularization to the loss and gradient
  loss += 0.5 * reg * np.sum(W * W)
  dW += reg*W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  num_class = W.shape[1]

  # Get score matrix
  scores = X.dot(W)

  # Subtract the max score for stability
  scores -= np.max(scores,axis = 1).reshape(num_train,1)

  # Get the exp scores
  exp_scores = np.exp(scores)/np.sum(np.exp(scores),axis = 1).reshape(num_train,1)

  # Get the softmax score which is the correct class normalized exp score
  softmax_score = exp_scores[range(num_train),y]

  # Compute loss
  loss = np.sum(-np.log(softmax_score))

  # Compute gradient
  # Compute the scale matrix of dW for all j
  Scale = exp_scores
  # Now for j == yi, subtract 1
  Scale[range(num_train),y] -= 1
  # Dot product to get dW
  dW = X.T.dot(exp_scores)



  # Right now the loss is a Wsum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  # Same with gradient
  dW /= num_train

  # Add regularization to the loss and gradient
  loss += 0.5 * reg * np.sum(W * W)
  dW += reg*W

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

