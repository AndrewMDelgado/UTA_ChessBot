import os
from Gui import GUI
from k2 import undistort
from templateMatching import Match

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
            if not self.isValid(diff):
                self.ID = -1
                return
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
    
    def promptCamera(self, preMove):
        moveDir = os.path.dirname(os.path.realpath(__file__)) + '/../phys/'
        if preMove:
            print('Capturing previous.jpg...')
            os.system("raspistill -o \"" + moveDir + "previous.jpg\"")
            print('Undistorting...')
            undistort(moveDir + 'previous.jpg')
            print('Complete.')
        else:
            print('Capturing current.jpg...')
            os.system("raspistill -o \"" + moveDir + "current.jpg\"")
            print('Undistorting...')
            undistort(moveDir + 'current.jpg')
            print('Complete. Generating differences.')
            self.matcher.genDiffs()
        
        '''
        if capt1:
            capture()
        else:
            capture2()
            self.matcher.genDiffs()
        '''
    
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
            if cleanDiff == []: #in theory, simply the blank line at EOF
                continue
            newDiff = self.Diff(cleanDiff)
            if newDiff.ID == -1:
                return 'Error reading position:\nMove not generated'
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
