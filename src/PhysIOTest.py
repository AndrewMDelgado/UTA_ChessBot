import PhysIO
import os

WHITE = True
BLACK = False

moveDir = os.path.dirname(os.path.realpath(__file__)) + '/../phys/'

plMoveSetW = [
    ['regMoveAC.txt', 'A2A3'],
    ['regMoveAE.txt', 'A3B4'],
    ['regMoveBD.txt', 'A7A6'],
    ['regMoveBF.txt', 'A6B5'],
    
    ['wCastleK.txt', 'O-O'],
    ['wCastleQ.txt', 'O-O-O'],
    ['wCastleExtraMove.txt', 'Too many pieces moved:\nE1 to G1\nH1 to F1\nG4 to G3'],
    ['bCastleK.txt', 'Invalid castle'],
    
    ['wPassantLeft.txt', 'B5A6EP'],
    ['wPassantRight.txt', 'B5C6EP'],
    ['bPassantLeft.txt', 'Invalid EP'],
    ['passantWrong.txt', 'Invalid EP']
]

plMoveSetB = [
    ['regMoveAC.txt', 'A2A3'],
    ['regMoveAE.txt', 'A3B4'],
    ['regMoveBD.txt', 'A7A6'],
    ['regMoveBF.txt', 'A6B5'],
    
    ['bCastleK.txt', 'O-O'],
    ['bCastleQ.txt', 'O-O-O'],
    ['bCastleExtraMove.txt', 'Too many pieces moved:\nE8 to G8\nH8 to F8\nA2 taken'],
    ['wCastleK.txt', 'Invalid castle'],
    
    ['bPassantLeft.txt', 'B4A3EP'],
    ['bPassantRight.txt', 'B4C3EP'],
    ['wPassantLeft.txt', 'Invalid EP'],
    ['passantWrong.txt', 'En passant: Invalid initial rank']
]

def testPhysIn(physIn, moveSet):
    passed = True
    for pair in moveSet:
        fname = moveDir + 'test/' + pair[0]
        expected  = pair[1]
        physIn.filename = fname
        actual = physIn.getPlayerMove()
        if expected != actual:
            passed = False
            print('Failure: ' + pair[0])
            print('\tExpected %s, got %s' % (expected, actual))
    return passed

physInW = PhysIO.PhysInput(WHITE)
physInB = PhysIO.PhysInput(BLACK)
wPassed = testPhysIn(physInW, plMoveSetW)
bPassed = testPhysIn(physInB, plMoveSetB)

if wPassed and bPassed:
    print('Success')
