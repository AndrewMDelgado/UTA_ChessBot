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
    
    ['wCastleK.txt', 'o-o'],
    ['wCastleQ.txt', 'o-o-o'],
    ['wCastleExtraMove.txt', 'invalid move type aaccd'],
    ['bCastleK.txt', 'invalid castle'],
    
    ['wPassantLeft.txt', 'B5A6EP'],
    ['wPassantRight.txt', 'B5C6EP'],
    ['bPassantLeft.txt', 'invalid EP'],
    ['passantWrong.txt', 'invalid EP']
]

plMoveSetB = [
    ['regMoveAC.txt', 'A2A3'],
    ['regMoveAE.txt', 'A3B4'],
    ['regMoveBD.txt', 'A7A6'],
    ['regMoveBF.txt', 'A6B5'],
    
    ['bCastleK.txt', 'o-o'],
    ['bCastleQ.txt', 'o-o-o'],
    ['bCastleExtraMove.txt', 'invalid move type bbbdd'],
    ['wCastleK.txt', 'invalid castle'],
    
    ['bPassantLeft.txt', 'B4A3EP'],
    ['bPassantRight.txt', 'B4C3EP'],
    ['wPassantLeft.txt', 'invalid EP'],
    ['passantWrong.txt', 'invalid EP']
]

def testPhysIn(physIn, moveSet):
    passed = True
    for pair in moveSet:
        fname = moveDir + pair[0]
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
