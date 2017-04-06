import numpy as np
from random import shuffle

def svm_loss_naive(W, X, y, reg):
  """
  Structured SVM loss function, naive implementation (with loops).

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

  """
  steps to implement vectorized loss and gradient computation
  1. initialize placeholder dW and loss
  2. compute score function
  3. compute margin function
  4. compute maximum compare between margin and 0
  5.1 sum up the margin > 0 equals total loss
  5.2 to get dW
      5.2.1 count the number of class scores did not meet the margin, dWyi equals to the
      Xi dimension scaled by this number
      5.2.1 count 1 for each of the class j's score did not meet the margin, dWj(j != yi)
      equals to the Xi dimension
      5.2.3 we construct an np array named count to store the above 2 steps counts
      count is 500x5 dimension, it stores the number of scale coefficient for each image
      5.2.4 dW = X.T.dot(count)
  """

  dW = np.zeros(W.shape) # initialize the gradient as zero

  # compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]
  loss = 0.0
  for i in xrange(num_train):
    scores = X[i].dot(W)
    correct_class_score = scores[y[i]]
    count = 0
    for j in xrange(num_classes):
      if j == y[i]:
        continue      
      margin = scores[j] - correct_class_score + 1 # note delta = 1
      if margin > 0:
        loss += margin
        dW[:,j] += X[i].T
        count += 1

    # Per http://cs231n.github.io/optimization-1/    
    dW[:,y[i]] -= count * X[i].T
  # Right now the loss is a Wsum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train

  # Same with gradient
  dW /= num_train

  # Add regularization to the loss.
  loss += 0.5 * reg * np.sum(W * W)
  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################
  # Gradient regularization that carries through per https://piazza.com/class/i37qi08h43qfv?cid=118
  dW += reg*W

  return loss, dW


def svm_loss_vectorized(W, X, y, reg):
  """
  Structured SVM loss function, vectorized implementation.

  Inputs and outputs are the same as svm_loss_naive.
  """

  # step 1
  dW = np.zeros(W.shape) # initialize the gradient as zero
  loss = 0.0 # initialize loss
  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################

  num_train = X.shape[0]
  num_class = W.shape[1]

  # step 2
  # Compute to get our score matrix
  vScores = X.dot(W)

  # step 3
  # get correct class score
  """
   Get the correct class score for each X,the V[range(a),range(b)] is a fast 2d indexing
   e.g. vScores[range(2),np.array([3,2])] is equivalent to
   np.array([vScores[0,3],vScores[1,2]])
  """
  vCorrect_class_score = vScores[range(num_train),y]
  # compute margin using broadcast
  vMargin = vScores - np.reshape(vCorrect_class_score,(num_train,1)) + 1
  # assign all the correct class margin entry as 0
  vMargin[range(num_train),y] = 0

  # step 4
  # compare element wise to get maximum
  # np.maximum compares 2 arrays and return element wise maximum of x1,x2
  maxMargin = np.maximum(np.zeros(vMargin.shape),vMargin)

  # step 5.1
  # sum up maximum loss
  loss = np.sum(maxMargin)

  # step 5.2.1
  # count 1 for each incorrect class scores which did not meet the margin
  count = maxMargin
  count[count>0] = 1

  # step 5.2.2
  # count number of class scores which did not meet the margi for each correct class
  col_sum = np.sum(count,axis = 1)

  # step 5.2.3
  # store the number to incorrect class to each correct class position for each image
  count[range(num_train),y] = -col_sum

  # step 5.2.4
  # get the dW
  """
   How to understand this dot product intuitively
   http://cs229.stanford.edu/section/cs229-linalg.pdf
   p5 formula 1
   p6 formula 3

   we get dW.shape = (50,5)
   each column is the derivative for corresponding class
  """
  dW = X.T.dot(count)

  # step 6
  # take the average and add reg to loss and dW
  # Right now the gradient is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  loss += 0.5 * reg * np.sum(W*W)

  dW /= num_train
  dW += reg*W



  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW
