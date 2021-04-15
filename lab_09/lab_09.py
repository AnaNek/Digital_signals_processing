"""
Image Deconvolution
"""

import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import convolve2d as conv2

from skimage import color, data, restoration, io

image = io.imread('bimage2.bmp')
image = color.rgb2gray(image)
psf = np.ones((8, 8)) / 81
image = conv2(image, psf, 'same')
image += 0.1 * image.std() * 0

deconvolved, _ = restoration.unsupervised_wiener(image, psf)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 5),
                       sharex=True, sharey=True)

plt.gray()

ax[0].imshow(image, vmin=deconvolved.min(), vmax=deconvolved.max())
ax[0].axis('off')
ax[0].set_title('Data')

ax[1].imshow(deconvolved)
ax[1].axis('off')
ax[1].set_title('Restored')

fig.tight_layout()

plt.show()
