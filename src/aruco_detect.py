import numpy as np
import cv2
import cv2.aruco as aruco
import os
moveDir = os.path.dirname(os.path.realpath(__file__)) + '/../phys/'

def detectCode():
    global moveDir
    #image = cv2.imread("start.jpeg")
    image = cv2.imread(moveDir + "previous.png")
    aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(
    image, aruco_dict, parameters=parameters)
    #print(corners, ids, rejectedImgPoints)
    aruco.drawDetectedMarkers(image, corners, ids)
    
    #aruco.drawDetectedMarkers(image, rejectedImgPoints, borderColor=(100, 0, 240))
    cv2.namedWindow('so52814747',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('so52814747',600,600)
    cv2.imshow('so52814747', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    '''
    #for i in corners:
     #   print(i)
    '''    
       

    return (ids,corners)
'''
if ids != None:
    rvec, tvec = aruco.estimatePoseSingleMarkers(corners, 0.6, camera_matrix, dist_coeffs)
    print(rvec,tvec)

for i in range(1,len(corners)):
    x = (corners[i-1][0][0][0] + corners[i-1][0][1][0] + corners[i-1][0][2][0] + corners[i-1][0][3][0]) / 4
    y = (corners[i-1][0][0][1] + corners[i-1][0][1][1] + corners[i-1][0][2][1] + corners[i-1][0][3][1]) / 4
    print(" x is: ", x, " y is: ", y)

'''
def detectCode2():
    global moveDir
    #image = cv2.imread("move2.jpeg")
    image = cv2.imread(moveDir + "current.png")
    aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(
    image, aruco_dict, parameters=parameters)
    #print(corners, ids, rejectedImgPoints)
    aruco.drawDetectedMarkers(image, corners, ids)
    
    #aruco.drawDetectedMarkers(image, rejectedImgPoints, borderColor=(100, 0, 240))
    cv2.namedWindow('so52814747',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('so52814747',600,600)
    cv2.imshow('so52814747', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    '''
    #for i in corners:
     #   print(i)
    '''    
       

    return (ids,corners)

