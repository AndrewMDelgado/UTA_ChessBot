import numpy as np
import cv2
import cv2.aruco as aruco
import os
from k2 import undistort
moveDir = os.path.dirname(os.path.realpath(__file__)) + '/../phys/'

def detectCode(filename):
    global moveDir
    #image = cv2.imread("start.jpeg")
    print('Reading ' + filename + '...')
    image = cv2.imread(moveDir + filename)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(
    image, aruco_dict, parameters=parameters)
    #print(corners, ids, rejectedImgPoints)
    print('Detecting markers...')
    aruco.drawDetectedMarkers(image, corners, ids)
    print('Complete.')
    
    #aruco.drawDetectedMarkers(image, rejectedImgPoints, borderColor=(100, 0, 240))
    cv2.namedWindow('so52814747',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('so52814747',600,600)
    cv2.imshow('so52814747', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    '''
    for i in corners:
        print(i)
    '''
    
    '''
    if ids != None:
        rvec, tvec = aruco.estimatePoseSingleMarkers(corners, 0.6, camera_matrix, dist_coeffs)
        print(rvec,tvec)

    for i in range(1,len(corners)):
        x = (corners[i-1][0][0][0] + corners[i-1][0][1][0] + corners[i-1][0][2][0] + corners[i-1][0][3][0]) / 4
        y = (corners[i-1][0][0][1] + corners[i-1][0][1][1] + corners[i-1][0][2][1] + corners[i-1][0][3][1]) / 4
        print(" x is: ", x, " y is: ", y)

    '''

    return (ids,corners)
