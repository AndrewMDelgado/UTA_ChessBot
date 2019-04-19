import os
from Gui import GUI
from capture import capture, capture2
from templateMatching import Match

class PhysInput_deprecated:

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

class PhysInput:

    kingIDs   = [1, 17]
    queenIDs  = [2, 18]
    bishopIDs = [3, 4, 19, 20]
    knightIDs = [5, 6, 21, 22]
    rookIDs   = [7, 8, 23, 24]
    pawnIDs   = [9, 10, 11, 12, 13, 14, 15, 16,
                25, 26, 27, 28, 29, 30, 31, 32]

    pieces = dict.fromkeys(kingIDs, 'K')
    pieces.update(dict.fromkeys(queenIDs, 'Q'))
    pieces.update(dict.fromkeys(bishopIDs, 'B'))
    pieces.update(dict.fromkeys(knightIDs, 'N'))
    pieces.update(dict.fromkeys(rookIDs, 'R'))
    pieces.update(dict.fromkeys(pawnIDs, 'P'))

    WHITE = True
    BLACK = False

    class Diff:
        def __init__(self, diff):
            assert self.isValid(diff)
            self.ID = int(diff[0])
            self.i  = diff[1]
            self.f  = diff[2]
        
        def __str__(self):
            diffStr = ''
            if self.taken():
                diffStr = self.i + ' taken'
            elif self.newPiece():
                diffStr = 'New piece at ' + self.f
            else:
                diffStr = self.i + ' to ' + self.f
            return diffStr
        
        def isValid(self, diff):
            def isSquare(sq):
                if len(sq) != 2:
                    return False
                elif sq == '__':
                    return True
                elif sq[0] in 'ABCDEFGH' and sq[1] in '12345678':
                    return True
                else:
                    return False
            
            if len(diff) != 3:
                return False

            diffID = diff[0]
            if not diffID.isdigit():
                return False
            elif int(diffID) < 0 or int(diffID) > 32:
                return False
            
            init = diff[1]
            finl = diff[2]
            if not (isSquare(init) and isSquare(finl)):
                return False
            
            return True
        
        def taken(self):
            return self.f == '__'
        
        def newPiece(self):
            return self.i == '__'
        
        def getColor(self):
            return self.ID < 17
        
        def getMoveStr(self):
            return self.i + self.f
            #if self.taken() or self.newPiece():
            #    return None
            #else:
            #    return self.i + self.f
    

    def __init__(self, playerColor):
        moveDir = os.path.dirname(os.path.realpath(__file__)) + '/../phys/'
        self.filename = moveDir + 'playerMove.txt'
        self.playerColor = playerColor
        self.matcher = Match()
    
    def promptCamera(self, capt1):
        if capt1:
            capture()
        else:
            capture2()
            self.matcher.genDiffs()
    
    def promptMove(self):
        temp = GUI(self)
        temp.promptMove()
    
    def regMove(self, diffA, diffB):
        if not diffB:
            if diffA.taken():
                return 'Piece illegally removed: ' + diffA.i
            else:
                return diffA.getMoveStr()
        
        #diffList has two diffs
        if diffB.taken() and diffA.f == diffB.i:
            return diffA.getMoveStr()
        elif diffA.taken() and diffB.f == diffA.i:
            return diffB.getMoveStr()
        else:
            return 'Player and opponent pieces moved,\nor taken piece still on board.'
    

    def castleMove(self, kingDiff, rookDiff):
        color = kingDiff.getColor()
        if color != self.playerColor:
            return 'Invalid castle'
        elif color == self.WHITE:
            if str(kingDiff) == 'E1 to G1' and str(rookDiff) == 'H1 to F1':
                return 'O-O'
            elif str(kingDiff) == 'E1 to C1' and str(rookDiff) == 'A1 to D1':
                return 'O-O-O'
            else:
                return 'Invalid castle'
        else:
            if str(kingDiff) == 'E8 to G8' and str(rookDiff) == 'H8 to F8':
                return 'O-O'
            elif str(kingDiff) == 'E8 to C8' and str(rookDiff) == 'A8 to D8':
                return 'O-O-O'
            else:
                return 'Invalid castle'


    def passantMove(self, pMoved, pTaken):
        fileList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        color = pMoved.getColor()
        if color != self.playerColor:
            return 'Invalid EP'
        moveRf = '6'
        takenRi = '5'
        if color == self.BLACK:
            moveRf = '3'
            takenRi = '4'
        fileDelta = abs(fileList.index(pMoved.i[0]) - fileList.index(pTaken.i[0]))

        if not (pMoved.i[1] == pTaken.i[1] == takenRi):
            return 'En passant: Invalid initial rank'
        if pMoved.f[1] != moveRf:
            return 'En passant: Invalid final rank'
        if fileDelta > 1:
            return 'En passant: Invalid initial file'
        if pMoved.f[0] != pTaken.i[0]:
            return 'En passant: Invalid final file'
        return pMoved.getMoveStr() + 'EP'


    def promotionMove(self, diffList):
        fileList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        pawnDiff = None
        newDiff = None
        takenDiff = None
        
        for diff in diffList:
            if self.pieces[diff.ID] == 'P':
                pawnDiff = diff
            elif diff.newPiece():
                newDiff = diff
            else:
                takenDiff = diff

        if not pawnDiff:
            moveStr = 'Too many pieces moved:'
            for diff in diffList:
                moveStr += '\n' + str(diff)
            return moveStr

        pawnColor = pawnDiff.getColor()
        
        pawnRi = '7'
        newRf = '8'
        if pawnColor == self.BLACK:
            pawnRi = '2'
            newRf = '1'

        pawnFi = pawnDiff.i[1]
        newFf = newDiff.f[1]
        fileDelta = abs(fileList.index(pawnFi) - fileList.index(newFf))

        if pawnDiff.i[0] != pawnRi:
            return 'Pawn ineligible for promotion.'
        elif newDiff.f[0] != newRf or fileDelta > 1:
            return 'Promoted pice at incorrect spot.'
        
        if takenDiff:
            if takenDiff.i != newDiff.f:
                return 'Piece illegally removed.'

        newPieceType = self.pieces[newDiff.ID]
        return pawnDiff.i + newDiff.f + '=' + newPieceType


    def hasNewPiece(self, diffList):
        for diff in diffList:
            if diff.newPiece():
                return True
        return False

    def processDiffs(self, diffList):
        if len(diffList) == 1:
            return self.regMove(diffList[0], None)
        
        diffA = diffList[0]
        diffB = diffList[1]
        opposed = (diffA.getColor() != diffB.getColor()) #pieces are opposite colors

        if not opposed:
            if self.pieces[diffA.ID] == 'K' and self.pieces[diffB.ID] == 'R':
                return self.castleMove(diffA, diffB)
            elif self.pieces[diffB.ID] == 'R' and self.pieces[diffB.ID] == 'K':
                return self.castleMove(diffB, diffA)
            else:
                return 'Two pieces of the same color moved.'
        
        #pieces are opposite colors
        if self.hasNewPiece(diffList):
            return self.promotionMove(diffList)
        
        if self.pieces[diffA.ID] == self.pieces[diffB.ID] == 'P':
            if diffB.taken():
                if diffB.i != diffA.f:
                    return self.passantMove(diffA, diffB)            
            elif diffA.taken():
                if diffA.i != diffB.f:
                    return self.passantMove(diffB, diffA)

        return self.regMove(diffA, diffB)
        

    def getPlayerMove(self, cam=True):
        if cam:
            self.promptCamera(False)
        else:
            self.promptMove()
        plFile = open(self.filename, "r")
        diffList = []
        for line in plFile:
            cleanDiff = line.strip().split()
            newDiff = self.Diff(cleanDiff)
            if not newDiff:
                return 'Invalid input'
            diffList.append(newDiff)
        plFile.close()

        moveStr = ''
        numDiffs = len(diffList)
        if numDiffs < 1:
            moveStr = 'No move made'
        elif numDiffs > 2:
            if numDiffs == 3 and self.hasNewPiece(diffList):
                moveStr = self.promotionMove(diffList)
            else:
                moveStr = 'Too many pieces moved:'
                for diff in diffList:
                    moveStr += '\n' + str(diff)
        else:
            moveStr = self.processDiffs(diffList)
        return moveStr



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
