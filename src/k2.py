import cv2
assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'
import numpy as np
from os.path import dirname, realpath
import glob
import sys
import matplotlib.pyplot as plt

# You should replace these 3 lines with the output in calibration step
def undistort(img_path):
    DIM=(2592, 1944)
    K=np.array([[1513.9004924448036, 0.0, 1394.4857784242886], [0.0, 1509.916904509583, 1069.4500493178837], [0.0, 0.0, 1.0]])
    D=np.array([[0.10584706040942171], [-1.1323548610571539], [3.4409205757758468], [-3.4001470724591547]])
    moveDir = dirname(realpath(__file__)) + '/../phys/'
    
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    plt.imsave(img_path, undistorted_img)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)
