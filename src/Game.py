from Board import Board
from InputParser import InputParser
from AI import AI
from GamePrep import GamePrep
from PhysIO import PhysInput, PhysOutput
import Gui
import sys
import random

gamePrep = GamePrep()
showBoard, twoPlayer, readBoard, quickStart, \
     variantGame, customGame = gamePrep.processTags(sys.argv)


def askForPlayerSide():
    WHITE = True
    BLACK = False
    playerChoiceInput = input(
        "What side would you like to play as [wB]? ").lower()
    if 'w' in playerChoiceInput:
        print("You will play as white")
        return WHITE
    else:
        print("You will play as black")
        return BLACK


def askForDepthOfAI():
    depthInput = 2
    try:
        depthInput = int(input("How deep should the AI look for moves?\n"
                               "Warning : values above 3 will be very slow."
                               " [2]? "))
    except KeyboardInterrupt:
        sys.exit()
    except:
        print("Invalid input, defaulting to 2")
    return abs(depthInput)


def printCommandOptions():
    undoOption = 'u : undo last move'
    printLegalMovesOption = 'l : show all legal moves'
    randomMoveOption = 'r : make a random move'
    printBoardOption = 'p : print the board'
    quitOption = 'quit : resign'
    moveOption = 'a3, Nc3, Qxa2, etc : make the move'
    options = [undoOption, printLegalMovesOption, randomMoveOption,
               printBoardOption, quitOption, moveOption, '', ]
    print('\n'.join(options))


def printAllLegalMoves(board, parser):
    for move in parser.getLegalMovesWithNotation(board.currentSide, short=True):
        print(move.notation)


def getRandomMove(board, parser):
    legalMoves = board.getAllMovesLegal(board.currentSide)
    randomMove = random.choice(legalMoves)
    randomMove.notation = parser.notationForMove(randomMove)
    return randomMove


def makeMove(move, board):
    print("Making move : " + move.notation)
    board.makeMove(move)

def printPointAdvantage(board):
    print("Currently, the point difference is : " +
          str(board.getPointAdvantageOfSide(board.currentSide)))

def saveGame(board):
    filename = input("Enter filename (.csg will be appended): ")
    filename = "../Saves/" + filename + ".csg"
    realName = gamePrep.saveGame(board, filename)
    print("Board state saved as " + realName)

def undoLastTwoMoves(board):
    if len(board.history) >= 2:
        board.undoLastMove()
        board.undoLastMove()

def specialCommands(cmd, board, parser):
    if command.lower() == 'u':
        undoLastTwoMoves(board)
    elif command.lower() == '?':
        printCommandOptions()
    elif command.lower() == 'l':
        printAllLegalMoves(board, parser)
    elif command.lower() == 'r':
        move = getRandomMove(board, parser)
        return False
    elif command.lower() == 'p':
        print()
        print(board)
        print()
    elif command.lower() == 's' or command.lower() == 'save':
        saveGame(board)
    return True


def display(msg, chessGUI, aiMove=False, useCam=False, useArm=False, title="Alert"):
    if not chessGUI:
        print(msg)
    elif aiMove:
        chessGUI.dispAIMove(msg, useCam=useCam, useArm=useArm)
    else:
        chessGUI.showinfo(title, msg)


def makeMoveReadable(move, board, aiMove, chessGUI=None,
                     useCam=False, physOutput=None):
    if aiMove:
        useArm = False
        if physOutput:
            useArm = True
            physOutput.movePieces(move)
        display("AI : " + str(move), chessGUI, aiMove=True,
                useCam=useCam, useArm=useArm)
    board.makeMove(move)


def minUIGame(board, playerSide, ai, useCamera, useMecArm):
    WHITE = True
    BLACK = False
    
    parserWhite = InputParser(board, WHITE)
    parserBlack = InputParser(board, BLACK)
    parser = parserWhite
    
    physInputWhite = PhysInput(WHITE)
    physInputBlack = PhysInput(BLACK)
    physInput = physInputWhite

    physOutput = None
    if useMecArm:
        physOutput = PhysOutput()
    
    PvP = not ai
    chessGUI = None
    if __name__ != '__main__':
        chessGUI = Gui.GUI(physInput)
    
    while True:
        if not chessGUI:
            if showBoard:
                print()
                print(board)
                print()
        if board.isCheckmate():
            if PvP:
                if board.currentSide == WHITE: #white has no legal moves
                    winner = 'Black'
                else:
                    winner = 'White'
                display("Checkmate! {} wins!".format(winner), chessGUI, title="Game Over")
            elif board.currentSide == playerSide:
                display("Checkmate, you lost", chessGUI, title="Game Over")
            else:
                display("Checkmate! You won!", chessGUI, title="Game Over")
            return

        if board.isStalemate():
            display("Stalemate", chessGUI, title="Game Over")
            return

        if PvP or board.currentSide == playerSide:
            # printPointAdvantage(board)
            if board.currentSide == WHITE:
                parser = parserWhite
                physInput = physInputWhite
                plRep = 'Wh'
            else:
                parser = parserBlack
                physInput = physInputBlack
                plRep = 'Bl'
            if not PvP:
                plRep = 'Pl'

            if chessGUI:
                chessGUI.physInput = physInput
                command = physInput.getPlayerMove(useCamera)
            else:
                command = input(plRep + " : ")
            
            move = None
            if command.lower() in ['u', '?', 'l', 'r', 'p', 's']:
                cont = specialCommands(command.lower(), board, parser)
                if cont:
                    continue
            elif command.lower() in ['exit', 'quit', 'q']:
                return
            
            try:
                move = parser.convertInput(command)
            except ValueError as error:
                display("{}\nCorrect your move and press OK.".format(error), chessGUI, title="Error")
                continue
            makeMoveReadable(move, board, False)
            if PvP:
                player = "WHITE"
                if board.currentSide == BLACK:
                    player = "BLACK"
                if useCamera:
                    physInput.promptCamera(True)
                chessGUI.showinfo("Next move", "{}, make your next move and press OK.".format(player))

        else:
            #print("AI thinking...")
            move = ai.getBestMove()
            move.notation = parser.notationForMove(move)
            makeMoveReadable(move, board, True, chessGUI,
                             useCam=useCamera, physOutput=physOutput)


def startFromGui(playerSide, aiDepth, useCamera, useMecArm):
    board = Board()
    opponentAI = None
    if aiDepth > 0: #0 indicates two-player game
        opponentAI = AI(board, not playerSide, aiDepth)
    minUIGame(board, playerSide, opponentAI, useCamera, useMecArm)

if __name__ == '__main__':
    if customGame:
        board = customGame
    else:
        mateInOne = (variantGame == 'mate')
        castleBoard = (variantGame == 'castle')
        passant = (variantGame == 'passant')
        promotion = (variantGame == 'promotion')
        board = Board(mateInOne, castleBoard, passant, promotion)

    try:
        playerSide = None
        aiDepth = None
        if quickStart:
            playerSide = quickStart[0]
            aiDepth = quickStart[1]
        else:
            playerSide = askForPlayerSide()
            print()
            aiDepth = askForDepthOfAI()
        opponentAI = None
        if not twoPlayer:
            opponentAI = AI(board, not playerSide, aiDepth)
        minUIGame(board, playerSide, opponentAI, False, False)
    except KeyboardInterrupt:
        sys.exit()
