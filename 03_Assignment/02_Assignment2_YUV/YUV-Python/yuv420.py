import numpy as np


def readYUV420(name: str, resolution: tuple, upsampleUV: bool = False):
    height = resolution[0]
    width = resolution[1]
    bytesY = int(height * width)
    bytesUV = int(bytesY/4)
    Y = []
    U = []
    V = []
    with open(name,"rb") as yuvFile:
        while (chunkBytes := yuvFile.read(bytesY + 2*bytesUV)):
            Y.append(np.reshape(np.frombuffer(chunkBytes, dtype=np.uint8, count=bytesY, offset = 0), (width, height)))
            U.append(np.reshape(np.frombuffer(chunkBytes, dtype=np.uint8, count=bytesUV, offset = bytesY),  (width//2, height//2)))
            V.append(np.reshape(np.frombuffer(chunkBytes, dtype=np.uint8, count=bytesUV, offset = bytesY + bytesUV), (width//2, height//2)))
    Y = np.stack(Y)
    U = np.stack(U)
    V = np.stack(V)
    if upsampleUV:
        U = U.repeat(2, axis=1).repeat(2, axis=2)
        V = V.repeat(2, axis=1).repeat(2, axis=2)
    return Y, U, V


# Y, U, V = readYUV420('data/dancing_org.1280x548.yuv', (1280, 548), True)
# # Y, U, V = readYUV420('data/dancing.640x274.yuv', (640, 274), True)
# # Y, U, V = readYUV420('data/dancing.320x138.yuv', (320, 138), True)
#
# Y2x = scipy.ndimage.zoom(Y, 2)
#
# print(f'Original dims: {Y.shape}, new dims: {Y2x.shape}')
#
# plt.imshow(Y2x[0], cmap='gray')
# plt.show()


def readYUV420Range(name: str, resolution: tuple, range: tuple, upsampleUV: bool = False):
    height = resolution[0]
    width = resolution[1]
    bytesY = int(height * width)
    bytesUV = int(bytesY/4)
    Y = []
    U = []
    V = []
    with open(name,"rb") as yuvFile:
        startLocation = range[0]
        endLocation = range[1] + 1
        startLocationBytes = startLocation * (bytesY + 2*bytesUV)
        endLocationBytes = endLocation * (bytesY + 2*bytesUV)
        data = np.fromfile(yuvFile, np.uint8, endLocationBytes-startLocationBytes, offset=startLocationBytes).reshape(-1,bytesY + 2*bytesUV)
        Y = np.reshape(data[:, :bytesY], (-1, width, height))
        U = np.reshape(data[:, bytesY:bytesY+bytesUV], (-1, width//2, height//2))
        V = np.reshape(data[:, bytesY+bytesUV:bytesY+2*bytesUV], (-1, width//2, height//2))
    if upsampleUV:
        U = U.repeat(2, axis=1).repeat(2, axis=2)
        V = V.repeat(2, axis=1).repeat(2, axis=2)
    return Y, U, V


def readYUV420RangePatches(name: str, resolution: tuple, frameRange: tuple, patchLoc: tuple, patchSize: tuple, upsampleUV: bool = False):
    width = resolution[0]
    height = resolution[1]
    patchLoc_w = patchLoc[0]
    patchLoc_h = patchLoc[1]
    patchSize_w = patchSize[0]
    patchSize_h = patchSize[1]
    bytesY = int(height * width)
    bytesUV = int(bytesY/4)
    bytesYUV = bytesY + 2*bytesUV
    Y = []
    U = []
    V = []
    startLocation = frameRange[0]
    endLocation = frameRange[1] + 1
    for frameCnt in range(startLocation, endLocation, 1):
        startLocationBytes = (frameCnt) * (bytesYUV)
        YPatches = []
        UPatches = []
        VPatches = []
        for _row in range(patchSize_h):
            offSetBytesStartY = (patchLoc_h * width) + patchLoc_w + startLocationBytes + (_row*width)
            offSetBytesEndY = offSetBytesStartY + patchSize_w
            with open(name,"rb") as yuvFile:
                YPatches.append(np.fromfile(yuvFile, np.uint8, offSetBytesEndY-offSetBytesStartY, offset=offSetBytesStartY).reshape(patchSize_w))
        for _row in range(patchSize_h//2):
            offSetBytesStartU = startLocationBytes + bytesY + (patchLoc_h//2 * width//2) +  patchLoc_w//2 + (_row*(width//2))
            offSetBytesEndU = offSetBytesStartU + patchSize_w//2
            offSetBytesStartV = startLocationBytes + bytesY + bytesUV + (patchLoc_h//2 * width//2) +  patchLoc_w//2 + (_row*(width//2))
            offSetBytesEndV = offSetBytesStartV + patchSize_w//2
            with open(name,"rb") as yuvFile:
                UPatches.append(np.fromfile(yuvFile, np.uint8, offSetBytesEndU-offSetBytesStartU, offset=offSetBytesStartU).reshape(patchSize_w//2))
            with open(name,"rb") as yuvFile:
                VPatches.append(np.fromfile(yuvFile, np.uint8, offSetBytesEndV-offSetBytesStartV, offset=offSetBytesStartV).reshape(patchSize_w//2))
        YPatches = np.reshape(np.concatenate(YPatches,0), (patchSize_w,patchSize_h))
        UPatches = np.reshape(np.concatenate(UPatches,0), (patchSize_w//2,patchSize_h//2))
        VPatches = np.reshape(np.concatenate(VPatches,0), (patchSize_w//2,patchSize_h//2))
        Y.append(YPatches), U.append(UPatches), V.append(VPatches)
    Y = np.stack(Y, 0)
    U = np.stack(U, 0)
    V = np.stack(V, 0)
    if upsampleUV:
        U = U.repeat(2, axis=1).repeat(2, axis=2)
        V = V.repeat(2, axis=1).repeat(2, axis=2)
    return Y, U, V


def writeYUV420(name: str, Y, U, V, downsample=True):
    Y = Y.astype(np.uint8)
    U = U.astype(np.uint8)
    V = V.astype(np.uint8)
    towrite = bytearray()
    if downsample:
        U = U[:, ::2, ::2]
        V = V[:, ::2, ::2]
    for i in range(Y.shape[0]):
        towrite.extend(Y[i].tobytes())
        towrite.extend(U[i].tobytes())
        towrite.extend(V[i].tobytes())
    with open(name, "wb") as destination:
        destination.write(towrite)


def RGB2YUV(rgb):
    m = np.array([[ 0.29900, -0.16874,  0.50000],
                 [0.58700, -0.33126, -0.41869],
                 [ 0.11400, 0.50000, -0.08131]])
    yuv = np.dot(rgb,m)
    yuv[:,:,:,1:]+=128.0
    yuv = np.clip(yuv,0,255)
    return yuv


def YUV2RGB(yuv):
    m = np.array([[ 1.0, 1.0, 1.0],
                 [-0.000007154783816076815, -0.3441331386566162, 1.7720025777816772],
                 [ 1.4019975662231445, -0.7141380310058594 , 0.00001542569043522235] ])
    
    rgb = np.dot(yuv,m)
    rgb[:,:,:,0]-=179.45477266423404
    rgb[:,:,:,1]+=135.45870971679688
    rgb[:,:,:,2]-=226.8183044444304
    rgb = np.clip(rgb,0,255)
    return rgb
