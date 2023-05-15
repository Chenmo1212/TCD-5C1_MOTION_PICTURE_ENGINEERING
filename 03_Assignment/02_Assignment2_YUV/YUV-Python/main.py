import numpy as np
import matplotlib.pyplot as plt
import scipy
from yuv420 import readYUV420, readYUV420Range, writeYUV420


# Y, U, V = readYUV420('data/dancing_org.1280x548.yuv', (1280, 548), True)
# Y, U, V = readYUV420('data/dancing.640x274.yuv', (640, 274), True)

ipt = "./yuv/dancing_640x274_96k.yuv"
opt = "./upsample/dancing_1280x720_from_640x274_96k.yuv"

Y, U, V = readYUV420Range(ipt, (640, 274), (0, 30), upsampleUV=True)
# Y, U, V = readYUV420(ipt, (640, 274), True)

Y2x = scipy.ndimage.zoom(Y, 2)
U2x = scipy.ndimage.zoom(U, 2)
V2x = scipy.ndimage.zoom(V, 2)
#
# print(f'Original dims: {Y.shape}, new dims: {Y2x.shape}')
# plt.imshow(Y2x[0], cmap='gray')
# plt.show()

# range = (0,30) # Frames 10 to 12 (inclusive)
# Y1, U1, V1 = readYUV420Range("path/file.yuv", (1920,1080), range, upsampleUV=True)


# Saving as YUV420 (Ensure Y, U, V arrays are 8 bit unsigned)
writeYUV420(opt, Y2x, U2x, V2x)