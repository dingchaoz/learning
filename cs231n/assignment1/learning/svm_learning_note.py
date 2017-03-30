"""
KNN must remember all training data and store it, this is space insufficient
also very expensive to test as it requires comparison to all training images.
therefore a more powerful approach that will natually extend to CNN consists of 
two major components: score function maps raw data to class scores and a loss
function that quantifies agreement between predicted score to truth.

high score or low score:
Intutively we wish higher score the more likely to be a class.

Interpreting linear classifier:
As the score is computed as a weighted sum of all pixels of 3 color channels; depending on
what valeus were set for the weight, the funciont has the capacity to like/dislike certain colors
at certain positions; for example, a ship classier would have a lot of positive weights across
blue channels in the surrounding areas of an image.

Analogy of images as high dimension points:
A line can reprsented as y = ax+b, where a is the slope, b is the tangent
or can be represented as ax+by+c = 0 and this is the right way when thinking about
each classifer is a line, and score of 0 means the image is right on the classifier line:
[a,b] * [x,
		 y]] + c
the write way written above in math is [a,b]T.dot([x,y]) + c

if ax+by+c >0, then the point is above the line, otherwise on or below the line
depending on the slope the point may be to the right or the left of the line

Interpretation of linear classifer as template matching:
if we draw the weights in each class, the rendered image is a template for that class
and the score is interpreted as comparing the image to the template, but instead of doing KNN, 
it uses the dot product as the distance instead of l1/l2 distance

Image data preprocessing:
very common to preform normaliztion of input feature(each pixel is a feature), it is IMPORTANT to
center the data by substracting the mean from every feature, and further preprocessing is to scale value
to [-1,1] range

Loss
SVM:
SVM is setup so that the correc class score for each image is higher than incorrect class by a margin
the standard svm loss is called hinge loss max(0,-), sometimes we use L2SVM, the squared version of hinge loss
which penalized viloted margins more strongly

Regularization:
The most appealing property is that penalizing large weights tends to improve generalization, because 
it means that no input dimension can have a large influence on the scores by itself.

Practical considerations:
setting delta margin to 1 as the magnitudes of W had direct effect on the scores and that magnitude is 
controlled by the regularization penalty.

"""