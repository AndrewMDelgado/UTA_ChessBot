import os

class PhysInput:

    class Diff:

        #State changes s:
        # a) W->E
        # b) B->E
        # c) E->W
        # d) E->B
        # e) B->W
        # f) W->B
        
        def __init__(self, diffStr):
            assert type(diffStr) == str and len(diffStr) == 3
            self.F = diffStr[0] #File A-H
            self.R = diffStr[1] #Rank 1-8
            self.s = diffStr[2] #state change a-f
            self.space = self.F + self.R
            self.state = diffStr
    
    class Move:
        def __init__(self, diffList):
            self.diffList = diffList
            self.diffList.sort(key = lambda diff: diff.s)
            self.stateList = []
            for diff in diffList:
                self.stateList.append(diff.state)

        def getMoveType(self):
            mTypeStr = ''
            for diff in self.diffList:
                mTypeStr += diff.s
            return mTypeStr #should be in alphabetical order
        
        def getDiffFromS(self, s):      #can't be used with castle
            for diff in self.diffList:
                if diff.s == s:
                    return diff
            return '[changed space not found]'
        
        def getRegMove(self, moveType, colorWhite):
            space_i = self.diffList[0].space
            space_f = self.diffList[1].space
            return space_i + space_f
        
        def getCastle(self, colorWhite):
            if colorWhite:
                kSideList = ['E1a', 'G1c', 'H1a', 'F1c']
                qSideList = ['E1a', 'C1c', 'A1a', 'D1c']
            else:
                kSideList = ['E8b', 'G8d', 'H8b', 'F8d']
                qSideList = ['E8b', 'C8d', 'A8b', 'D8d']
            
            if set(kSideList) == set(self.stateList):
                return 'o-o'
            elif set(qSideList) == set(self.stateList):
                return 'o-o-o'
            else:
                return 'invalid castle'

        def getPassant(self, moveType, colorWhite):
            fileStr = 'ABCDEFGH'
            
            pawnDest = self.diffList[2].space
            destF = pawnDest[0]
            destR = pawnDest[1]

            if colorWhite:
                plPawn = self.diffList[0].space
                aiPawn = self.diffList[1].space
                delta = 1 #rank movement for en passant
                correctRank = '5'
            else:
                plPawn = self.diffList[1].space
                aiPawn = self.diffList[0].space
                delta = -1
                correctRank = '4'
            plF = plPawn[0]
            aiF = aiPawn[0]
            plR = plPawn[1]
            aiR = plPawn[1]
            
            fileDiff = fileStr.index(plF) - fileStr.index(aiF)
            sameRank = (plR == aiR == correctRank)
            adjacent = (abs(fileDiff) == 1)
            correctDest = (destF == aiF and int(destR) == int(aiR) + delta)
            
            if sameRank and adjacent and correctDest:
                return plPawn + pawnDest + 'EP'
            else:
                return 'invalid EP'
    
    def __init__(self, playerColor):
        moveDir = os.path.dirname(os.path.realpath(__file__)) + '/../phys/'
        self.filename = moveDir + 'playerMove.txt'
        self.playerColor = playerColor
    
    def promptCamera(self):
        return 0
        #TODO: wait for player to finish turn, call camera prog to generate playerMove.txt

    def getPlayerMove(self):
        self.promptCamera()
        plFile = open(self.filename, "r")
        diffList = []
        for line in plFile:
            diffList.append(self.Diff(line.strip()))
        plFile.close()
        
        move = self.Move(diffList)
        regMoves = ['ac', 'ae', 'bd', 'bf']
        castles  = ['aacc', 'bbdd']
        passants = ['abc', 'abd']
        
        moveType = move.getMoveType()
        if moveType in regMoves:
            return move.getRegMove(moveType, self.playerColor)
        elif moveType in castles:
            return move.getCastle(self.playerColor)
        elif moveType in passants:
            return move.getPassant(moveType, self.playerColor)
        else:
            return 'invalid move type ' + moveType #will register as invalid move
        #TODO: Implement pawn promotion



class PhysOutput:
    
    def __init__(self):
        self.a = 5



class VirtualBoard:
    class VirtualPiece:
        def __init__(self, color, x, y):
            self.color = color
            self.x = x
            self.y = y

    fileStr = 'ABCDEFGH'
    def __init__(self):
        self.grid = [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['-', '-', '-', '-', '-', '-', '-', '-'],
            ['p', 'p', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]
    
    def __str__(self):
        gridStr = ''
        for rank in reversed(self.grid):
            for space in rank:
                gridStr += space
            gridStr += '\r\n'
        return gridStr
