import chess
import chess.engine

class ChessLogic:
    def __init__(self):
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci("/usr/local/opt/stockfish/bin/stockfish")
        self.last_move = None

    # Returns move in 'chess.Move' format
    def getBestMove(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
        best_move = result.move
        return best_move

        
    def quitEngine(self):
        self.engine.quit()
    
    # Takes move in 'chess.Move' format
    def validateMove(self, move):
        return move in self.board.legal_moves
    
    # Takes move in string format
    def movePiece(self, move):
        move = chess.Move.from_uci(move)
        self.last_move = move  # Update last_move attribute
        self.board.push(move)
    
    def get_board(self):
        return self.board
    
    def reset_board(self):
        self.board = chess.Board()
    
    def check_mate(self):
        return self.board.is_checkmate()

    def getOutcome(self):
    #.winner returns true for white win, false for black, None for draw
        if self.board.outcome():
            #Transforming outcome() to satisfactory format
            result = str(self.board.outcome().termination).split('.')
            result = result[1].replace('_', ' ').title()
            return result
        
    def checkSpecialMove(self):
        if self.last_move and self.last_move.from_square == chess.E1 and self.last_move.to_square == chess.G1:
            print("Last move was kingside castling.")
            return True
        if self.last_move and self.last_move.from_square == chess.E1 and self.last_move.to_square == chess.C1:
            print("Last move was queenside castling.")
            return True
        if self.last_move and self.board.is_en_passant(self.last_move):
            print("Last move was an en passant capture.")
            return True
        if self.last_move and self.last_move.promotion:
            print("Last move was a promotion move.")
            return True
        
if __name__ == "__main__":
    chessLogic = ChessLogic()
    while True:
        print(chessLogic.get_board())
        move = chessLogic.getBestMove()
        #print(move)
        chessLogic.movePiece(move.uci())
        if chessLogic.checkSpecialMove():
            break  # Check special move after making the move
        result = chessLogic.getOutcome()
        if result:
            print(result)
            break
        print(chessLogic.get_board())

    chessLogic.quitEngine()