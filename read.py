
import numpy as np
import  matplotlib.pyplot as plt
import matplotlib.image as img
 
#视觉法图像灰度化
def imgGray_Version(im):
    """
    image gray
    im: source image
    Return gray image.
    """
    imgarray = np.array(im, dtype = np.float32)
    rows = im.shape[0]
    cols = im.shape[1]
    for i in range(rows):
        for j in range(cols):
            imgarray[i, j, :] = (imgarray[i, j, 0] * 0.299 + imgarray[i, j, 1] * 0.587 + imgarray[i, j, 2] * 0.114)
    return imgarray.astype(np.uint8)
 
im = img.imread("./data/test.jpg")#图像读取
im = imgGray_Version(im)
plt.imshow(im)#图像显示
img.imsave('./save/save.jpg',im)