# YUV-Python
Simple function for reading in YUV 420 Files in Python

## Usage
Takes in path to YUV file and resolution of the file (eg. 1920x1080) and returns three numpy arrays, one for Y, U and V channels of dimensions (# of frames * height * width) for Y and (# of frames * height/2 * width/2) for U and V. You can also upsample to include full sized U and V arrays.

readYUV420 reads the entire sequence into memory

readYUV420Range reads the range into memory


```python
from yuv420 import readYUV420, readYUV420Range, writeYUV420

Yarr, Uarr, Varr = readYUV420("path/file.yuv", (1920,1080), upsampleUV=True)


range = (10,12) # Frames 10 to 12 (inclusive)
Yarr1, Uarr1, Varr1 = readYUV420Range("path/file.yuv", (1920,1080), range, upsampleUV=True)


# Saving as YUV420 (Ensure Y, U, V arrays are 8 bit unsigned)
writeYUV420("path/modified.yuv" , Yarr1, Uarr1, Varr1)
```
