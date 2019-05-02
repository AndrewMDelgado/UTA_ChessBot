import numpy as np
from os.path import dirname, realpath
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import sys
chessRoot = dirname(realpath(__file__)) + '/'
sys.path.insert(0, chessRoot + 'src/')
from templateMatching import Match

defished = chessRoot + 'init.jpg'
fullImg = mpimg.imread(defished)
fullImgGray = np.dot(fullImg[...,:3], [0.229, 0.587, 0.114])

whiteout = [] #Populate with str such as 'A1' or 'C4'
for i in range(1, len(sys.argv)):
    whiteout.append(sys.argv[i])

def inImg(i, j, img):
    inX = (0 <= i < len(img[0]))
    inY = (0 <= j < len(img))
    return inX and inY

def fillSquare(img, sq, val):
    for j in range(sq.minY(), sq.maxY()):
        for i in range(sq.minX(), sq.maxX()):
            if inImg(i, j, img):
                try:
                    img[j][i] = val
                except IndexError:
                    pass

sqVals = open(chessRoot + 'sqVals.txt', "w")
fileList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
virtualBoard = Match().board
for r, row in enumerate(virtualBoard):
    for f, sq in enumerate(row):
        sqVals.write(str(sq) + ': ' + str(sq.topL) + ' to ' + str(sq.botR) + '\n')
        spaceVal = r + f + 1
        isOdd = bool(spaceVal % 2)
        if isOdd:
            fillSquare(fullImgGray, sq, 0)
        if str(sq) in whiteout:
            fillSquare(fullImgGray, sq, 255)
sqVals.close()

plt.figure(3)
plt.imshow(fullImgGray, cmap=plt.get_cmap('gray'))
plt.show()
