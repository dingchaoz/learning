"""
KNN must remember all training data and store it, this is space insufficient
also very expensive to test as it requires comparison to all training images.
therefore a more powerful approach that will natually extend to CNN consists of 
two major components: score function maps raw data to class scores and a loss
function that quantifies agreement between predicted score to truth.

high score or low score:
Intuitively we wish higher score the more likely to be a class.

Interpreting linear classifier:
As the score is computed as a weighted sum of all pixels of 3 color channels; depending on
what values were set for the weight, the function has the capacity to like/dislike certain colors
at certain positions; for example, a ship classier would have a lot of positive weights across
blue channels in the surrounding areas of an image.

Analogy of images as high dimension points:
A line can represented as y = ax+b, where a is the slope, b is the tangent
or can be represented as ax+by+c = 0 and this is the right way when thinking about
each classifier is a line, and score of 0 means the image is right on the classifier line:
[a,b] * [x,
		 y]] + c
the write way written above in math is [a,b]T.dot([x,y]) + c

if ax+by+c >0, then the point is above the line, otherwise on or below the line
depending on the slope the point may be to the right or the left of the line

Interpretation of linear classifier as template matching:
if we draw the weights in each class, the rendered image is a template for that class
and the score is interpreted as comparing the image to the template, but instead of doing KNN, 
it uses the dot product as the distance instead of l1/l2 distance

Image data pre-processing:
very common to preform normalization of input feature(each pixel is a feature), it is IMPORTANT to
center the data by subtracting the mean from every feature, and further pre-processing is to scale value
to [-1,1] range

Loss
SVM:
SVM is setup so that the correct class score for each image is higher than incorrect class by a margin
the standard svm loss is called hinge loss max(0,-), sometimes we use L2SVM, the squared version of hinge loss
which penalized violated margins more strongly

Regularization:
The most appealing property is that penalizing large weights tends to improve generalization, because 
it means that no input dimension can have a large influence on the scores by itself.

Practical considerations:
setting delta margin to 1 as the magnitudes of W had direct effect on the scores and that magnitude is 
controlled by the regularization penalty.

"""

import numpy as np
W = np.random.randn(50,5)
X = np.random.randn(500,50)
y = np.random.randint(5,size = 500)
reg = 0.1

"""
steps to implement vectorized loss and gradient computation
1. initialize placeholder dW and loss
2. compute score function
3. get correct class score and compute margin function
4. compute maximum compare between margin and 0
5.1 sum up the margin > 0 equals total loss
5.2 to get dW
    5.2.1 count 1 for each incorrect class scores which did not meet the margin, dWj(j != yi)
    equals to the Xi dimension
    5.2.2 count the number of class scores did not meet the margin, dWyi equals to the
    Xi dimension scaled by this number
    5.2.3 we construct an np array named count to store the above 2 steps counts
    count is 500x5 dimension, it stores the number of scale coefficient for each image
    5.2.4 dW = X.T.dot(count)
6. take the average and add reg to loss and dW
"""
# step 1
dW = np.zeros(W.shape) # initiate a placeholder for gradient of weights
loss = 0

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
# store the number to incorrect class to each corret class position for each image
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
loss /= num_train
loss += 0.5 * reg * np.sum(W*W)

dW /= num_train
dW += reg*W

print dW, loss







