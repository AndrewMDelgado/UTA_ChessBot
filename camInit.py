#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 14:48:33 2018

@author: lenangungu
"""
import numpy as np
import time
import os
#from aruco_detect import detectCode
#from aruco_detect import detectCode2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import skimage.feature as sk

initName = os.path.dirname(os.path.realpath(__file__)) + "/init.jpeg"
os.system("raspistill -o \"" + initName + "\"")
fullImg = mpimg.imread(initName)
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
fullImgGray = rgb2gray(fullImg)
#plt.imshow(fullImgGray, cmap = plt.get_cmap('gray'))
#plt.show()

colMax = 446 #change depending on picture 
rowMax = 324

colMin = 592
rowMin = 480


#print("(",rowMax,"," ,colMax,")")


    
topL = [colMax,rowMax]
botR = [colMin,rowMin] 

topLi = topL
botRi = botR
board = []

#WILL TURN THIS PROCESS OF MAKING THE ROWN IN A FUNCTION LATE 

#Creating row A
#A = [[(topL,botR,'A1')]]
A = [[topL,botR,'A1']]
for i in range (2,9):
    #xtopL = [i*topL[0],topL[1]]
    xtopL = [botRi[0],topLi[1]]
    #xbotR = [(i+1)*topL[0],botR[1]]
    xbotR = [botRi[0]+ (botRi[0]-topLi[0]),botRi[1]]
    
    A.append((xtopL,xbotR,('A'+ str(i)))) 
    topLi = xtopL
    botRi = xbotR
   

#Creating row B  
topL2 = [topL[0],topL[1] + (botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + (botR[1]-topL[1])]
topLi = topL2
botRi = botR2
board.append(A)


B = [[topL2,botR2,'B1']] 

for i in range (2,9):
    
    #xtopL = [i*topL2[0],topL2[1]]
    #xbotR = [(i+1)*topL2[0],botR2[1]]
    xtopL = [botRi[0],topLi[1]]
    xbotR = [botRi[0]+ (botRi[0]-topLi[0]),botRi[1]]
    topLi = xtopL
    botRi = xbotR
    B.append((xtopL,xbotR,('B'+ str(i)))) 
board.append(B)
    
#Creating row C   

topL2 = [topL[0],topL[1] + 2*(botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + 2*(botR[1]-topL[1])]
topLi = topL2
botRi = botR2

C = [[topL2,botR2,'C1']]
    
for i in range (2,9):
    xtopL = [botRi[0],topLi[1]]
    xbotR = [botRi[0]+ (botRi[0]-topLi[0]),botRi[1]]
    topLi = xtopL
    botRi = xbotR
    
    C.append((xtopL,xbotR,('C'+ str(i)))) 
board.append(C)


#Creating row D   

topL2 = [topL[0],topL[1] + 3*(botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + 3*(botR[1]-topL[1])]
topLi = topL2
botRi = botR2

D = [[topL2,botR2,'D1']]
    
for i in range (2,9):
    xtopL = [botRi[0],topLi[1]]
    xbotR = [botRi[0]+ (botRi[0]-topLi[0]),botRi[1]]
    topLi = xtopL
    botRi = xbotR
    
    D.append((xtopL,xbotR,('D'+ str(i)))) 
board.append(D)

#Creating row E   

topL2 = [topL[0],topL[1] + 4*(botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + 4*(botR[1]-topL[1])]
topLi = topL2
botRi = botR2

E = [[topL2,botR2,'E1']]
    
for i in range (2,9):
    xtopL = [botRi[0],topLi[1]]
    xbotR = [botRi[0]+ (botRi[0]-topLi[0]),botRi[1]]
    topLi = xtopL
    botRi = xbotR
    
    E.append((xtopL,xbotR,('E'+ str(i)))) 
board.append(E)

#Creating row F   

topL2 = [topL[0],topL[1] + 5*(botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + 5*(botR[1]-topL[1])]
topLi = topL2
botRi = botR2

F = [[topL2,botR2,'F1']]
    
for i in range (2,9):
    xtopL = [botRi[0],topLi[1]]
    xbotR = [botRi[0]+ (botRi[0]-topLi[0]),botRi[1]]
    topLi = xtopL
    botRi = xbotR
    
    F.append((xtopL,xbotR,('F'+ str(i)))) 
board.append(F)

#Creating row G   

topL2 = [topL[0],topL[1] + 6*(botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + 6*(botR[1]-topL[1])]
topLi = topL2
botRi = botR2

G = [[topL2,botR2,'G1']]
    
for i in range (2,9):
    xtopL = [botRi[0],topLi[1]]
    xbotR = [botRi[0]+ (botRi[0]-topLi[0]),botRi[1]]
    topLi = xtopL
    botRi = xbotR
    
    G.append((xtopL,xbotR,('G'+ str(i)))) 
board.append(G)

#Creating row H   

topL2 = [topL[0],topL[1] + 7*(botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + 7*(botR[1]-topL[1])]
topLi = topL2
botRi = botR2

H = [[topL2,botR2,'H1']]
    
for i in range (2,9):
    xtopL = [botRi[0],topLi[1]]
    xbotR = [botRi[0]+ (botRi[0]-topLi[0]),botRi[1]]
    topLi = xtopL
    botRi = xbotR
    
    H.append((xtopL,xbotR,('H'+ str(i)))) 
board.append(H)


img_copy = fullImg 

#This is to make sure the board is stored correctly     
for i in range (A[0][0][1], A[0][1][1]):
    for u in range (A[0][0][0],(A[0][1][0])):
        img_copy[i][u] = 0

for i in range (A[3][0][1], A[3][1][1]):
    for u in range (A[3][0][0],(A[3][1][0])):
        img_copy[i][u] = 0
   
   
    
plt.figure(3)
fullImgGray = rgb2gray(img_copy)        
plt.imshow(fullImgGray, cmap = plt.get_cmap('gray'))
plt.show()

'''
#TO OPTIMIZE, USE CENTER OF ARUCO AND SQUARE ON BOARD
#Algorithm to see what square aruco code falls in
#Aruco returns four corners of the ID 
'''
