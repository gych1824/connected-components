#!/usr/bin/env python
import numpy as np
import pylab as plt
import time
import cc

def test_image():
    # create a test image
    tic = time.clock()

    x = np.linspace(-1, 1, 1201)        # about the size of the SeaRISE-Antarctica dataset
    xx, yy = np.meshgrid(x, x)

    I = np.zeros_like(xx, dtype='f8')

    for x0,y0,r0 in np.random.rand(25,3):
        x0 = x0*2 - 1
        y0 = y0*2 - 1
        r0 *= 0.25
        I[(xx-x0)**2 + (yy-y0)**2 < r0**2] = 2 # "floating ice"

    for x0,y0,r0 in np.random.rand(25,3):
        x0 = x0*2 - 1
        y0 = y0*2 - 1
        r0 *= 0.25
        I[(xx-x0)**2 + (yy-y0)**2 < r0**2] = 1 # add some "land"

    toc = time.clock()
    return I, (toc - tic)

I, t = test_image()
print "Preparing input took %f s" % t

# original
plt.figure(figsize=(12,4))
plt.subplot(1,3,1)
plt.imshow(np.ma.array(I,mask=I==0),
           interpolation='nearest')
plt.xticks([])
plt.yticks([])
plt.title("original image")
plt.xlabel("land is blue, floating ice is red")

# labeled components
tic = time.clock()
result1 = cc.cc(I)
toc = time.clock()
print "Computing labels took %f s" % (toc - tic)

plt.subplot(1,3,2)
plt.imshow(np.ma.array(result1, mask=result1==0),
           interpolation='nearest')
plt.xticks([])
plt.yticks([])
plt.title("labeled image")
plt.xlabel("a unique label for each component")

# "iceberg" identification
tic = time.clock()
result2 = cc.cc(I, identify_icebergs=True)
toc = time.clock()
print "Computing labels took %f s" % (toc - tic)

plt.subplot(1,3,3)
plt.imshow(np.ma.array(result2, mask=result2==0),
           interpolation='nearest')
plt.xticks([])
plt.yticks([])
plt.title("icebergs")

plt.tight_layout(pad=2, w_pad=1)
plt.show()
