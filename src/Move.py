class Move:

    def __init__(self, piece, newPos, pieceToCapture=None):
        self.notation = None
        self.check = False
        self.checkmate = False
        self.kingsideCastle = False
        self.queensideCastle = False
        self.promotion = False
        self.passant = False
        self.stalemate = False

        self.piece = piece
        self.oldPos = piece.position
        self.newPos = newPos
        self.pieceToCapture = pieceToCapture
        # For en passant and castling
        self.specialMovePiece = None
        # For castling
        self.rookMove = None

    def old_str(self):
        displayString = 'Old pos : ' + str(self.oldPos) + \
                        ' -- New pos : ' + str(self.newPos)
        if self.notation:
            displayString += ' Notation : ' + self.notation
        if self.passant:
            displayString = 'Old pos : ' + str(self.oldPos) + \
                            ' -- New pos : ' + str(self.newPos) + \
                            ' -- Pawn taken : ' + str(self.specialMovePiece)
            displayString += ' PASSANT'
        return displayString
    
    def __str__(self):
        def rankOfPos(pos):
            return str(pos[1] + 1)

        def fileOfPos(pos):
            transTable = str.maketrans('01234567', 'abcdefgh')
            return str(pos[0]).translate(transTable)
        
        if self.kingsideCastle or self.queensideCastle:
            return str(self.notation)
        
        displayString = fileOfPos(self.oldPos) + rankOfPos(self.oldPos)
        displayString += fileOfPos(self.newPos) + rankOfPos(self.newPos)
        if self.passant:
            displayString += 'EP'
        elif self.promotion:
            displayString += '=' + self.specialMovePiece.stringRep
        
        return displayString


    def __eq__(self, other):
        if self.oldPos == other.oldPos and \
           self.newPos == other.newPos and \
           self.specialMovePiece == other.specialMovePiece:
            if not self.specialMovePiece:
                return True
            if self.specialMovePiece and \
               self.specialMovePiece == other.specialMovePiece:
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):
        return hash((self.oldPos, self.newPos))

    def reverse(self):
        return Move(self.piece, self.piece.position,
                    pieceToCapture=self.pieceToCapture)
