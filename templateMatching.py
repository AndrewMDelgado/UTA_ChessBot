#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 14:48:33 2018

@author: lenangungu
"""
import numpy as np


import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import skimage.feature as sk

fullImg = mpimg.imread('board.jpeg')
img_copy = np.copy(fullImg)

smallImg =  mpimg.imread('square.png')
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

fullImgGray = rgb2gray(fullImg) 
smallImgGray = rgb2gray(smallImg)
#plt.figure(1)
plt.imshow(fullImgGray, cmap = plt.get_cmap('gray'))
#plt.figure(2)
plt.imshow(smallImgGray, cmap = plt.get_cmap('gray'))


coor = sk.match_template(fullImgGray,smallImgGray)
colMax = np.argmax(np.max(coor, axis=0))
rowMax = np.argmax(np.max(coor, axis=1))


#print("(",rowMax,"," ,colMax,")")

l = len(smallImg) 
l = l * 2 #for some reason algortihm only detected half of the square. Timing it by two game me the whole square
'''
for i in range (rowMax,rowMax + l):
    for u in range (colMax,(colMax) + l):
        img_copy[i][u] = 0
'''        
topL = [colMax,rowMax]
botR = [ colMax + l, rowMax + l ]
#print("Top left corner of first square: ", topL, "Bottom right  corner of first square: ", botR)

board = []

#WILL TURN THIS PROCESS OF MAKING THE ROWN IN A FUNCTION LATE 

#Creating row A
#A = [[(topL,botR,'A1')]]
A = [[topL,botR,'A1']]
for i in range (2,9):
    xtopL = [i*topL[0],topL[1]]
    xbotR = [(i+1)*topL[0],botR[1]]
    
    A.append((xtopL,xbotR,('A'+ str(i)))) 

#Creating row B  
topL2 = [topL[0],topL[1] + (botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + (botR[1]-topL[1])]
board.append(A)

#B = [[(topL,botR,'B1')]] - NOT WORKING
B = [[topL2,botR2,'B1']] 

for i in range (2,9):
    xtopL = [i*topL2[0],topL2[1]]
    xbotR = [(i+1)*topL2[0],botR2[1]]
    
    B.append((xtopL,xbotR,('B'+ str(i)))) 
board.append(B)
    
#Creating row C   

topL2 = [topL[0],topL[1] + 2*(botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + 2*(botR[1]-topL[1])]

C = [[topL2,botR2,'C1']]
    
for i in range (2,9):
    xtopL = [i*topL2[0],topL2[1]]
    xbotR = [(i+1)*topL2[0],botR2[1]]
    
    C.append((xtopL,xbotR,('C'+ str(i)))) 
board.append(C)

#Creating row D   

topL2 = [topL[0],topL[1] + 3*(botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + 3*(botR[1]-topL[1])]

D = [[topL2,botR2,'D1']]
    
for i in range (2,9):
    xtopL = [i*topL2[0],topL2[1]]
    xbotR = [(i+1)*topL2[0],botR2[1]]
    
    D.append((xtopL,xbotR,('D'+ str(i)))) 
board.append(D)

#Creating row E   

topL2 = [topL[0],topL[1] + 4*(botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + 4*(botR[1]-topL[1])]

E = [[topL2,botR2,'E1']]
    
for i in range (2,9):
    xtopL = [i*topL2[0],topL2[1]]
    xbotR = [(i+1)*topL2[0],botR2[1]]
    
    E.append((xtopL,xbotR,('E'+ str(i)))) 
board.append(E)

#Creating row F   

topL2 = [topL[0],topL[1] + 5*(botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + 5*(botR[1]-topL[1])]

F = [[topL2,botR2,'F1']]
    
for i in range (2,9):
    xtopL = [i*topL2[0],topL2[1]]
    xbotR = [(i+1)*topL2[0],botR2[1]]
    
    F.append((xtopL,xbotR,('F'+ str(i)))) 
board.append(F)

#Creating row G   

topL2 = [topL[0],topL[1] + 6*(botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + 6*(botR[1]-topL[1])]

G = [[topL2,botR2,'G1']]
    
for i in range (2,9):
    xtopL = [i*topL2[0],topL2[1]]
    xbotR = [(i+1)*topL2[0],botR2[1]]
    
    G.append((xtopL,xbotR,('G'+ str(i)))) 
board.append(G)

#Creating row H   

topL2 = [topL[0],topL[1] + 7*(botR[1]-topL[1])]
botR2 = [botR[0],botR[1] + 7*(botR[1]-topL[1])]

H = [[topL2,botR2,'H1']]
    
for i in range (2,9):
    xtopL = [i*topL2[0],topL2[1]]
    xbotR = [(i+1)*topL2[0],botR2[1]]
    
    H.append((xtopL,xbotR,('H'+ str(i)))) 
board.append(H)


'''
#This is to make sure the board is stored correctly     
for i in range (H[3][0][1],H[3][1][1]):
    for u in range (H[3][0][0],H[3][1][0]):
        img_copy[i][u] = 0
       
        
plt.figure(3)
fullImgGray = rgb2gray(img_copy)        
plt.imshow(fullImgGray, cmap = plt.get_cmap('gray'))
'''

'''
#TO OPTIMIZE, USE CENTER OF ARUCO AND SQUARE ON BOARD
#Algorithm to see what square aruco code falls in
#Aruco returns four corners of the ID 
#let a be return from aruco 
a = [[100, 479], [150, 479],[100, 500], [150,500]]
currentSquare = ''
square_ids = []  

#this is for each id in corners (reference from aruco_detect)
for i in range (0,8):
    row = board[i] # e.g A
    for j in range (0,8):
        square1 = row[j] # e.g A1
        #square2 = row[j+1] # e.g A2
        #print("a: ",a[0][0], "sq1: ",square1[0][0],"sq2: ",square2[0][0])
        
        if ((a[0][0] > square1[0][0]) and (a[0][0] < square1[1][0])):
            if((a[0][1] > square1[0][1]) and (a[0][1] < square1[1][1])):
                currentSquare = square1[2]
                i = 9 #terminate both loops
                j = 8 #terminate both loops
        
            
pair = [id,currentSquare]            
      
print("The id", id, " is in square: ", currentSquare)

'''




