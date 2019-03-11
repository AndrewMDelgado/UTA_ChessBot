from Board import Board
from Pawn import Pawn
from Rook import Rook
from King import King
from Bishop import Bishop
from Knight import Knight
from Queen import Queen
from Coordinate import Coordinate as C
from InputParser import InputParser
import re
import os

WHITE = True
BLACK = False


class GamePrep:
    def loadGame(self, filename):
        board = Board()
        board.pieces.clear()
        parserWhite = InputParser(board, WHITE)
        parserBlack = InputParser(board, BLACK)
        
        gameFile = open(filename, "r")
        lines = []
        for line in gameFile:
            lines.append(line)
        gameFile.close()
        
        histStr = lines[8]
        currentSide = ('W' == histStr[0])
        board.currentSide = currentSide

        pieceDict = dict.fromkeys(['p', '0', '1', '6', '7'], Pawn)
        pieceDict.update(dict.fromkeys(['k'], Knight))
        pieceDict.update(dict.fromkeys(['b'], Bishop))
        pieceDict.update(dict.fromkeys(['r', '2', '3', '8', '9'], Rook))
        pieceDict.update(dict.fromkeys(['q'], Queen))
        pieceDict.update(dict.fromkeys(['k', '4', '5', 'm'], King))

        for i in range(8):
            for j, p in enumerate(lines[i]):
                if p == '-':
                    continue
                coords = C(j, i)
                movesMade = 0
                if p.isalpha():
                    side = p.isupper() #WHITE if True, else BLACK
                    if p.lower() == 'm': #king on either side
                        movesMade = 2
                    
                    #movesMade += 1 + int(p.isupper()) #movesMade = 1 or 2 based on p's case
                    #if p.lower() in "ab" and ((side == WHITE and coords[1] == 1) \
                    #    or (side == BLACK and coords[1] == 6)): #proves p is a pawn that hasn't moved
                    #    movesMade = 0
                else:
                    numP = int(p)
                    side = (numP % 2 == 0) #WHITE if True, else BLACK
                    movesMade = 1 + int(numP > 5)

                board.pieces.extend(pieceDict[p.lower()](board, side, coords, movesMade))
        
        #TODO: Process last move to enter into board.history
        return board
    

    def saveGame(self, board, filename):
        def replaceChar(s, i, r):
            return s[:i]+r+s[i+1:]
        
        def getPieceNewRep(piece):
            importantMovers = "PpRrKk"
            p = piece.stringRep
            if piece.side == BLACK:
                p = p.lower()
            
            mover = piece.movesMade > 0
            traveler = piece.movesMade > 1
            if mover and p in importantMovers:
                pIdx = importantMovers.index(p)
                if traveler:
                    pIdx += 6
                    if pIdx == 10:
                        pIdx = 'M' #Monarch
                    if pIdx == 11:
                        pIdx = 'm'
                p = str(pIdx)
            return p

        gameFile = open(filename, "w")
        filepath = os.path.abspath(gameFile.name)
        pieceStr = "----------------------------------------------------------------"
        for piece in board.pieces:
            p = getPieceNewRep(piece)
            pos = piece.position[0] + (8 * piece.position[1])
            pieceStr = replaceChar(pieceStr, pos, p)
        for i in range(8):
            fin = 64 - (i * 8)
            init = fin - 8
            gameFile.write(pieceStr[init:fin] + '\n')

        if board.currentSide == WHITE:
            histStr = "B "
        else:
            histStr = "W "
        
        dashes = "-----"
        takenStr = "-"
        if board.history:
            lastMove = board.getLastMove()
            lastMoveStr = str(lastMove)
            if lastMove.passant:
                lastMoveStr = lastMoveStr[:4] + 'P'
            elif lastMove.promotion:
                lastMoveStr = lastMoveStr[:4] + lastMoveStr[5]
            
            idx = len(lastMoveStr)
            histStr += lastMoveStr + dashes[idx:]
            pieceTaken = lastMove.pieceToCapture
            if pieceTaken:
                takenStr = getPieceNewRep(pieceTaken)
        else:
            histStr += dashes
        
        histStr += takenStr
        gameFile.write(histStr)
        gameFile.close()
        return filepath


    def processTags(self, argv):
        showBoard  = not "--hb" in argv
        twoPlayer = "--two" in argv
        
        qsRegEx = re.compile('--qs(w|W|b|B)[1-3]$')
        quickStart = None
        for arg in argv:
            if qsRegEx.match(arg):
                quickStart = [WHITE, 1]
                if arg[4] == 'b' or arg[4] == 'B':
                    quickStart[0] = BLACK
                quickStart[1] = int(arg[5])

        variantGame = ""
        customGame = None
        if "--vg" in argv:
            variantGame = input(
                "Variant game? [mate, castle, passant, promotion, custom]: ").lower()
            #if variantGame == 'custom':
            #    filename = input("Enter custom game filename: ")
            #    customGame = self.loadGame(filename)
        
        return showBoard, twoPlayer, quickStart, variantGame, customGame

