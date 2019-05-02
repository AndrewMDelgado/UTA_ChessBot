import numpy as np
from os.path import dirname, realpath
from aruco_detect import detectCode
#from statistics import mean

class Match:
    def __init__(self):
        self.board = self.createBoard()
        self.root = dirname(realpath(__file__)) + '/../'
        
    class Square:
        def __init__(self, topL, botR, r, f):
            self.file = f
            self.rank = r
            self.topL = topL
            self.botR = botR
        
        def __str__(self):
            return self.file + self.rank
        
        def minX(self):
            return self.topL[0]
        
        def maxX(self):
            return self.botR[0]
        
        def minY(self):
            return self.topL[1]
        
        def maxY(self):
            return self.botR[1]
    
    def createBoard(self):
        filename = dirname(realpath(__file__)) + '/../firstSq.txt'
        firstSqFile = open(filename, "r")

        firstSq = []
        for line in firstSqFile:
            firstSq.append(line)
        firstSqFile.close()
        
        topLStr = firstSq[0].strip().split()
        botRStr = firstSq[1].strip().split()

        bTopL = [int(topLStr[0]), int(topLStr[1])]
        bBotR = [int(botRStr[0]), int(botRStr[1])]
        lenX = bBotR[0] - bTopL[0]
        lenY = bBotR[1] - bTopL[1]
        board = []

        fileList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        for idx_r in range(8):
            row = []
            r = str(8 - idx_r)
            minY = bTopL[1] + (idx_r * lenY)
            for idx_f, f in enumerate(fileList):
                minX = bTopL[0] + (idx_f * lenX)
                sqTopL = [minX, minY]
                sqBotR = [minX + lenX, minY + lenY]
                row.append(self.Square(sqTopL, sqBotR, r, f))
            #board.append(row)
            board = [row] + board

        return board
    
    def position(self, cornerArr): #TODO
        def mean(vals):
            s = sum(vals)
            m = s / len(vals)
            return m

        corners = cornerArr[0]
        x_avg = mean(list(c[0] for c in corners))
        y_avg = mean(list(c[1] for c in corners))
        center = [int(x_avg), int(y_avg)]

        for row in self.board:
            for sq in row:
                #print(str(sq) + ': ' + str(sq.topL) + ' ' + str(sq.botR)
                if (sq.minX() <= center[0] < sq.maxX()) and (sq.minY() <= center[1] < sq.maxY()):
                    return str(sq)
        return str(center)
    
    def genDiffs(self):
        changes = []
        ids1, prevS_unsorted = detectCode('previous.jpg')
        ids2, currS_unsorted  = detectCode('current.jpg')

        if ids1 == None or ids2 == None:
            moveDir = dirname(realpath(__file__)) + '/../phys/'
            filename = moveDir + 'playerMove.txt'
            output = open(filename, "w")
            output.write('Error: No pieces detected.')
            output.close()
            return

        ids1 = ids1.astype(int).ravel()
        ids2 = ids2.astype(int).ravel()
        prevZip = sorted(zip(ids1, prevS_unsorted))
        currZip = sorted(zip(ids2, currS_unsorted))

        #get sorted lists for IDs and States
        idsPrev = [ID for ID, _ in prevZip]
        idsCurr = [ID for ID, _ in currZip]
        previousState = [corners for _, corners in prevZip]
        currentState = [corners for _, corners in currZip]

        if idsPrev == idsCurr: #no pieces taken; piece ostensibly moved
            for i in range(len(currentState)):
                isStill = np.array_equal(previousState[i][0], currentState[i][0])
                if not isStill:
                    pos1 = self.position(previousState[i])
                    pos2 = self.position(currentState[i])
                    changes.append((idsPrev[i], pos1, pos2))
        
        else: #piece removed from or added to board
            for i, ID in enumerate(idsPrev):
                stillHere = (ID in idsCurr)
                if stillHere:
                    j = idsCurr.index(ID)
                    isStill = np.array_equal(previousState[i], currentState[j])
                    if not isStill:
                        pos1 = self.position(previousState[i])
                        pos2 = self.position(currentState[j])
                        changes.append((idsPrev[i], pos1, pos2))
                else:
                    pos1 = self.position(previousState[i])
                    pos2 = '__'
                    changes.append((ID, pos1, pos2))

            for i, ID in enumerate(idsCurr):
                alreadyHere = (ID in idsPrev)
                if not alreadyHere:
                    pos1 = '__'
                    pos2 = self.position(currentState[i])

        moveDir = dirname(realpath(__file__)) + '/../phys/'
        filename = moveDir + 'playerMove.txt'
        output = open(filename, "w")
        for c in changes:
            #print(c)
            if c[1] != c[2]:
                output.write(str(c[0]) + ' ' + str(c[1]) + ' ' + str(c[2]) + '\n')
        output.close()
