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
  loss = 0.0
  dW = np.zeros(W.shape) # initialize the gradient as zero
  vdW = np.zeros(W.shape) # initialize the gradient as zero
  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################
   # compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]
  loss = 0.0
  vScores = X.dot(W)

  """
  Get the correct class score for each X,the V[range(a),range(b)] is a fast 2d indexing
  e.g. vScores[range(2),np.array([3,2])] is equivalent to
  np.array([vScores[0,3],vScores[1,2]])

  """
  vCorrect_class_score = vScores[range(num_train), y]

  # Broadcast to compute margin
  vMargin = vScores - np.reshape(vCorrect_class_score,(num_train,1)) + 1

  """
  method 1

  """
  # assign all the correct class margin entry as 0
  vMargin[range(num_train),y] = 0

  # np.maximum compares 2 arrays and return element wise maximum of x1,x2
  maxMargin = np.maximum(np.zeros(vMargin.shape),vMargin)

  # sum up to a scalar loss value
  loss = np.sum(maxMargin)


  """
  method 2

  # if j == y[i] do not include in loss (or dW)
  mask = np.zeros(vMargin.shape)
  mask[range(num_train),y] = 1
  loss = (vMargin-mask)[vMargin>0].sum()
  """


  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train

  # Add regularization to the loss.
  loss += 0.5 * reg * np.sum(W * W)

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################


  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  #############################################################################
  """
  Vectorized version
  """


  count = maxMargin

  # If original binary value > 0 meaning marginal >0, then we need to count that
  # as 1 penalty, this way we binarize the thresh array ending with either 0 or 1
  # 0 in pos(i,j) means the ith image 's jth class score is good already no loss

  count[count > 0] = 1

  # Sum up by column for each row, we get the count of the number of classes
  # that didn’t meet the desired margin (and hence contributed to the loss function)
  col_sum = np.sum(count,axis = 1)

  # Pass col sum into binary, the bad class scores for each image is passed into
  # the correct class  position, and now each element of binary is the penalty or
  # derivative coefficient for each class for each image
  count[range(num_train),y] = -col_sum

  """
  How to understand this dot product intuitively
  http://cs229.stanford.edu/section/cs229-linalg.pdf
  p5 formula 1
  p6 formula 3

  we get dW.shape = (50,5)
  each column is the derivative for corresponding class
  """
  dW = X.T.dot(count)

  """

  for method

  vdW = np.zeros(W.shape)
  i,j = np.nonzero(vMargin>0)
  for ii,jj in zip(i,j):
    vdW[:,y[ii]] -= X[ii,:]
    vdW[:,jj] += X[ii,:]

  idx = (j == y[i])
  vdWCorr = np.zeros(W.shape)# if j == y[i]
  for ii,jj in zip(i[idx],j[idx]):
    vdWCorr[:,y[ii]] += X[ii,:]
    vdWCorr[:,jj] -= X[ii,:]

  vdW -= vdWCorr
  dW = vdW


  """

  # Right now the gradient is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  dW /= num_train
  # Add regularization to the gradient.
  dW += reg*W

  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW
