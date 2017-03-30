"""
03/30/2017
Assignment 1, KNN
Lecture 1

KNN classifier consists of two stages, during training the classifier the training data and simply remembers it, during testing, the classifier takes every image by comparing to all training images and transferring the labels of the k most similar training objects.

Writing def compute_distances_no_lopps(self,X) function in k_nearest_neighbor.py 
This function computes distance between each test point with training points with no explicit loops.
Inputs:
X: the test image arrays, in a shape of (500,3072) 500 images, each image 3072 dimension
X_train: the training image arrays, in a shape of (5000,3072), 5000 images
Outputs:
	dists: (500,5000), which is initialized as np.zeros((num_test,num_train))

Overview
Suppose we have only 1 test image X of 3d and 1 train images X_train of 3d
X = [[1,2,3]]
X_train = [[1.5,2.5,3.5]]

the euclidean distance of X to X_train would be
sqrt((1-1.5)^2 + (2-2.5)^2 + (3-3.5)^2)
now expand it
sqrt(1^2+1.5^2- 2*1*1.5 + 2^2+2.5^2- 2*2*2.5 + 3^2+3.5^2 - 2*3*3.5)
Examing above we see that it is equvalent to:
sum square pixels of test image + sum square pixels of train - 2* dot product of test and train pixels
"""

### demo code 

# intilize
import numpy as np
X = np.random.randn(500,3072)
X_train = np.random.randn(5000,3072)

"""
Compute the distance between each test point in X and each training point
in self.X_train using no explicit loops.

Input / Output: Same as compute_distances_two_loops
"""
num_test = X.shape[0]
num_train = X_train.shape[0]
dists = np.zeros((num_test, num_train)) 
#########################################################################
#                                                                #
# Compute the l2 distance between all test points and all training      #
# points without using any explicit loops, and store the result in      #
# dists.                                                                #
#                                                                       #
# You should implement this function using only basic array operations; #
# in particular you should not use functions from scipy.                #
#                                                                       #
# HINT: Try to formulate the l2 distance using matrix multiplication    #
#       and two broadcast sums.                                         #
#########################################################################

"""
Square all pixels and take a sum across each row
we get (500,) a rank 1 array SqSumXtest, each element is the squared sum of each test images' pixels
"""

SqSumXtest = np.sum(X**2,axis = 1)

"""
Square all pixels and take a sum across each row
we get (5000) SqSumXtest, each row is the squared sum of each train images' pixels
"""

SqSumXtrain = np.sum(X_train**2,axis = 1) 

"""
The dots product need to end up in a (500,5000) shape and we are givin (500,3072) and
we were given X(500) and X_train (5000,3072), so the only way would be 
X.dot(X_train.T)
"""
 
dots = X.dot(X_train.T) 

"""
This is where the broadcast occurs
http://cs231n.github.io/python-numpy-tutorial/#numpy-broadcasting
Broadcating is a powerful mechanism that allows numpy to work with arrays of different shapes when
performing arithmetic operations. Frequently we haev a smaller array and a larger array, and we want
to use the smaller array multiple times to perform some operation on the larger array
Broadcasting alows computation performed without actually creating multiple copies of smaller array

Now let's examine the shapes of the 3 arrays we got
dots is the array of the ideal size already (500,5000)
the other 2 are smaller

Think of SqSumXtrain (5000,) already matches with the number of columns of dots
so these two can be broadcasted directly: SqSumXtrain will be automatialy copied 500 times and be added to each of th 500 rows
of dots;

Think of SqSumXtest(500,) which is a rank 1 array, this can be a bit tricky
rank 1 array (500,) written out is [x1,x2,.....x500], it is essentially a 1 d array with out 2nd d
rank 2 array(1,500) written out is [[x1,x2,...x500]], it is a 2 d array with the fist d 1, 2nd d 500
(500,) matches with the number of rows of dots, we need to reshape it so it can be broadcasted

The X.reshape(num_test,1) is equivalent to X[:,None] or X[:,np.newaxis] or
instead of reshape X, we can transpose dots, then transpose back like:
dots.T.dot(X).T

"""
dists = SqSumXtest.reshape(num_test,1)- 2*dots + SqSumXtrain


#########################################################################
#                         END OF YOUR CODE                              #
#########################################################################
print dists