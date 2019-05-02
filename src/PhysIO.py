import os
from os.path import dirname, realpath
from Gui import GUI
from k2 import undistort
from templateMatching import Match

class PhysInput:

    kingIDs   = [0, 16]
    queenIDs  = [1, 17]
    bishopIDs = [2, 3, 18, 19]
    knightIDs = [4, 5, 20, 21]
    rookIDs   = [6, 7, 22, 23]
    pawnIDs   = [8, 9, 10, 11, 12, 13, 14, 15,
                24, 25, 26, 27, 28, 29, 30, 31]

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
            elif int(diffID) < 0 or int(diffID) > 31:
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
            return self.ID < 16
        
        def getMoveStr(self):
            return self.i + self.f
            #if self.taken() or self.newPiece():
            #    return None
            #else:
            #    return self.i + self.f
    

    def __init__(self, playerColor):
        moveDir = dirname(realpath(__file__)) + '/../phys/'
        self.filename = moveDir + 'playerMove.txt'
        self.playerColor = playerColor
        self.matcher = Match()
    
    def promptCamera(self, preMove):
        moveDir = dirname(realpath(__file__)) + '/../phys/'
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
    
    def __init__(self, aiColor):
        self.aiColor = aiColor
        self.board = Match().board
        self.heights = {
            'K':0,
            'Q':1,
            'B':2,
            'N':4,
            'R':6,
            'P':8
        }

    def movePiece(self, piece, oldPos, newPos):
        sq1 = None
        sq2 = None
        coord1 = []
        coord2 = []
        
        if oldPos == '__':
            coord1 = '[Reserves]'
        else:
            sq1 = self.board[oldPos[1]][oldPos[0]]
            xVal = (sq1.minX() + sq1.maxX()) / 2
            yVal = (sq1.minY() + sq1.maxY()) / 2
            coord1 = [xVal, yVal]
        
        if newPos == '__':
            coord2 = '[Graveyard]'
        else:
            sq2 = self.board[newPos[1]][newPos[0]]
            xVal = (sq2.minX() + sq2.maxX()) / 2
            yVal = (sq2.minY() + sq2.maxY()) / 2
            coord2 = [xVal, yVal]
        
        height = self.heights[piece.stringRep]
        #move piece from coord1 to coord2 according to height
        print(str(coord1) + ' to ' + str(coord2) + ' (height ' + str(height) + ')')

        

    def processMove(self, move):
        print('Moving piece: ' + str(move))
        if move.kingsideCastle or move.queensideCastle:
            rook = move.specialMovePiece
            yVal = move.oldPos[1]
            xVal = 5 if move.kingsideCastle else 2
            self.movePiece(move.piece, move.oldPos, move.newPos)
            self.movePiece(rook, rook.position, [xVal, yVal])
        elif move.passant:
            enmPawn = move.specialMovePiece
            self.movePiece(move.piece, move.oldPos, move.newPos)
            self.movePiece(enmPawn, enmPawn.position, '__')
        elif move.promotion:
            self.movePiece(move.piece, move.oldPos, '__')
            # make move.specialMovePiece(?) or just prompt player to put piece down
        elif move.pieceToCapture:
            taken = move.pieceToCapture
            self.movePiece(taken, taken.position, '__')
            self.movePiece(move.piece, move.oldPos, move.newPos)
        else:
            self.movePiece(move.piece, move.oldPos, move.newPos)

