import numpy as np
from os import system
from os.path import dirname, realpath
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import sys
chessRoot = dirname(realpath(__file__)) + '/'
sys.path.insert(0, chessRoot + 'src/')
import k2

initName = chessRoot + 'init.jpg'
system("raspistill -o \"" + initName + "\"")
k2.undistort(initName)
#defished = chessRoot + 'phys/undistorted.jpg'

fullImg = mpimg.imread(initName)
fullImgGray = np.dot(fullImg[...,:3], [0.229, 0.587, 0.114])

plt.figure(3)
plt.imshow(fullImgGray, cmap=plt.get_cmap('gray'))
plt.show()
