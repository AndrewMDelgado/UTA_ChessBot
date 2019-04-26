#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 14:48:33 2018

@author: lenangungu
"""
import numpy as np
import time
#from aruco_detect import detectCode
#from aruco_detect import detectCode2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import skimage.feature as sk



fullImg = mpimg.imread('setup.jpeg')
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
fullImgGray = rgb2gray(fullImg) 
plt.imshow(fullImgGray, cmap = plt.get_cmap('gray'))

"""
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

'''
coor = sk.match_template(fullImgGray,smallImgGray)
colMax = np.argmax(np.max(coor, axis=0))
rowMax = np.argmax(np.max(coor, axis=1))
'''
colMax = 41 #change depending on picture 
rowMax = 338


#print("(",rowMax,"," ,colMax,")")


    
topL = [colMax,rowMax]
#botR = [ colMax + l, rowMax + l ]
botR = [121,415]

'''   
l = len(smallImg) 
l = l * 2 #for some reason algortihm only detected half of the square. Timing it by two game me the whole square


for i in range (rowMax,botR[1]):
    for u in range (colMax,botR[0]):
        img_copy[i][u] = 0

'''
topLi = topL
botRi = botR
#print("Top left corner of first square: ", topL, "Bottom right  corner of first square: ", botR)

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

#B = [[(topL,botR,'B1')]] - NOT WORKING
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



#This is to make sure the board is stored correctly     
for i in range (H[7][0][1], H[7][1][1]):
    for u in range (H[7][0][0],(H[7][1][0])):
        img_copy[i][u] = 0
       
        
plt.figure(3)
fullImgGray = rgb2gray(img_copy)        
plt.imshow(fullImgGray, cmap = plt.get_cmap('gray'))


'''
#TO OPTIMIZE, USE CENTER OF ARUCO AND SQUARE ON BOARD
#Algorithm to see what square aruco code falls in
#Aruco returns four corners of the ID 
'''
#call aruco detect to get ids and corresponding corners
#ids,corners = detectCode()
currentSquare = ''
square_ids = []  

'''
#this is for each id in corners (reference from aruco_detect)
for i in range (0,8):
    row = board[i] # e.g A
    for j in range (0,8):
        square1 = row[j] # e.g A1
        #square2 = row[j+1] # e.g A2
        #print("a: ",a[0][0], "sq1: ",square1[0][0],"sq2: ",square2[0][0])
        
        if ((corners[i][0][0][0] > square1[0][0]) and (corners[i][0][0][0] < square1[1][0])):
            if((corners[i][0][0][1] > square1[0][1]) and (corners[i][0][0][1] < square1[1][1])):
                currentSquare = square1[2]
                pair = [ids[i],currentSquare]
                print("The id", ids[i], " is in square: ", currentSquare)
                square_ids.append(pair)
                i = 9 #terminate both loops
                j = 8 #terminate both loops
'''        
            

#Have aruco detect make a 2D array of id,corners 
#Call aruco_detect and return ids with corresponding coordinates  and save as previous state
changes = []
ids1, previousState = detectCode()

#after a user move, call aruco_detect and save as current state

ids2, currentState = detectCode2()
idsPrev = ids1
idsCurr = ids2

ids1 = ids1.astype(int)
ids1 = ids1.ravel()
ids1.sort()

ids2 = ids2.astype(int)
ids2 = ids2.ravel()
ids2.sort()

print("ids1: ",ids1)
print("uds2: ",ids2)
#Run algorithm to detect move 
if (len(previousState) == len(currentState)):
    print("same length")
    #find which id changed coordinates 
    for i in range(0, len(previousState)):
        
        #if pieces move slightly, that will also be considered as a change in coordinate so if we have more than one change we need to look more into it 
        if previousState[i][0].any() != currentState[i][0].any(): #Assuming the ids are ordered, if not then order them using a function  

            changes.append(currentState[i])
        else:
            pass
            #print("Previous state: ",previousState[i][0])
            #print("Current state: ", currentState[i][0])

#Use changes array to classify the new position of pieces (create a classify function that returns ids and squares they are in)            
else:
    print(len(previousState),len(currentState))
   
    
    
    for i in range (0,len(ids1)):
        current = ids1[i]
        j = 0
        f = 0 
        for j in range (0,len(ids2)):
            if current == ids2[j]:
                f = 1
                #check if coordinates changed
                #if yes, then add to change addray with old and new coordinates (id,from,to)
                print(current,ids2[j])
            else:
                j += 1
                
        if f == 0:
            #get coordinates from corners of previous state
            #classify square and have (id,from,null) - meaning piece was removed 
            changes.append(current)        


print(changes)

'''
	//store new state (id, coordinate) in a new matrix
	//First check if any piece was removed by checking the number of items in previous state and current state
	//If the number is the same (a move with no loss of piece)
		//find which id changed coordinates (ID5,A7,A8)
		//map that coordinate to a square in the game (small algorithm for this)
	//if the number is not the same (a piece has been removed)
		//find out which piece not in the new state  (ID5, A7, _) 
		//signal the AI that the piece is not available anymore
		//check for a change in coordinate 
		//map that coordinate to a square in the game (small algorithm for this)
	
'''
"""
