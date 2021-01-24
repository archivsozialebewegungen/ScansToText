Numpy arrays
============

Stripped down to basics, images are just arrays - two-dimensional arrays in
case of grayscale or black-and-white images, multidimensional arrays for
color images or images with an alpha channel (for transparency).

So to manipulate images in one kind or another, we have to manipulate arrays -
which is quite slow, if you run for-loops over large images. Here numpy
comes into focus: Numpy is (among other things) a python implementation of
arrays, that allow fast transformation of these arrays. So most implementations
of image manipulation algorithms use numpy arrays for greater speed.

This is obviously a good thing, but it has some drawbacks. For once, numpy
arrays (or ndarray, as they are commonly called) are just arrays and not
images. You may infer that a boolean ndarray represents a black-and-white
image, a uint8 array a grayscale image and a three dimensional array a
RGB color image - but this is just guesswork. And you have no information at
all about the resolution or the color scheme.

So working with numpy arrays to manipulate images always involves tracking
this information. This is the main reason why we use the PIL Image class
in this project whenever we transport image data between modules and functions.

Another drawback is the quirky syntax for manipulationg numpy arrays,
that is quite counterintuitive. I will document some of these quirks for
my own sanity in the following chapters.

Special selectors
-----------------

Selecting parts of an image
...........................

Let's assume you want to cut out a part of an image. The image has
the dimensions 600x800 pixels. The upper left corner is always
the coordinate 0|0, the lower right corner is 600|800 in our case.

Now we want do cut out a rectangle
where the left upper pixel has the coordinate 20|40 and the right
lower pixel has the coordinate 60|80. In this case we may specify
our cutout like this:

  cutout_array = img_array[20:60, 40:80]
  
Do not use the coordinates as parameters! We deal with an array,
so the first parameter is the range of the x values, the second
parameter is the range of y values.

And it is important, that the cutout is not a new object but just
a view of the original data, so by changing the cutout, you also
change the original data. You need to use the <code>copy()</code>
method on the array to get a new array.

Using arrays as selectors
.........................

In a nutshell: If you use an array as selector, you get an array
in return with the dimensions of the selector array where the
values are the values of the original array that are indexed by
the selector array values.

This sounds confusing and it is. Take this example:

	original = np.array([0, 1, 2, 3, 4])
	selector = np.array([1, 3, -2])
	print(original[selector])
	
This results in <code>[1, 3, 3]</code>, the negative value counting
from the end.

When using one dimensional arrays, this is still quite intuitive,
but on multi dimensional array it may get really confusing.


Using logical selectors
.......................

But not only the regualar python slicing and striding syntax is
working, but also some other puzzling expressions are possible.
For example what does an expression like the following mean?

  ndarray1[ndarray2 > 127] = True
  
This is a handy way to transform a grayscale image to a black-and-white image.
If <code>ndarray1</code> is an array initialized with <code>False</code> and
<code>ndarray2</code> is a grayscale image of the same dimensions, then for
all elements in the array <code>ndarray2</code>, where the element is greater
that 127, the corresponding element in <code>ndarray1</code> is set to
<code>True</code>.

So the selector in the square brackets allows for selecting pixels in an
<code>ndarray</code>. This is used a lot quite a lot in image manipulation,
so we need to get used to this syntax.

 
  