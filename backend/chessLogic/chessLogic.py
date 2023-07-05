import chess
import chess.engine
class ChessLogic:
    def __init__(self, STOCKFISH_PATH):
        self.board = chess.Board()
        self.last_move = None
        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        #self.engine.configure({"Skill Level": 5})

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
        
    def getWinner(self):
        outcome = self.board.outcome()
        if outcome is not None:
            if outcome.winner == chess.WHITE:
                return 'white'
            elif outcome.winner == chess.BLACK:
                return 'black'
            else:
                return 'draw'
        else:
            return None

    def checkSpecialMove(self):
        if self.last_move and self.last_move.from_square == chess.E1 and self.last_move.to_square == chess.G1:
            rookMove = "h1f1"
            print("Last move was kingside castling.")
            return rookMove
        if self.last_move and self.last_move.from_square == chess.E1 and self.last_move.to_square == chess.C1:
            rookMove = "a1d1"
            print("Last move was queenside castling.")
            return rookMove
        if self.last_move and self.last_move.from_square == chess.E8 and self.last_move.to_square == chess.G8:
            rookMove="h8f8"
            print("Last move was black kingside castling.")
            return rookMove
        if self.last_move and self.last_move.from_square == chess.E8 and self.last_move.to_square == chess.C8:
            rookMove = "a8d8"
            print("Last move was black queenside castling.")
            return rookMove
        if self.last_move and self.board.is_en_passant(self.last_move):
            print("Last move was an en passant capture.")
            return True
        if self.last_move and self.last_move.promotion:
            print("Last move was a promotion move.")
            return True
        
if __name__ == "__main__":
    STOCKFISH_PATH = "/usr/local/opt/stockfish/bin/stockfish"
    chessLogic = ChessLogic(STOCKFISH_PATH)
    while True:
        print(chessLogic.get_board())
        move = chessLogic.getBestMove()
        #print(move)
        chessLogic.movePiece(move.uci())
        if chessLogic.checkSpecialMove():
            print(chessLogic.get_board())
            print(chessLogic.last_move)
            print(move)
            break  # Check special move after making the move
        result = chessLogic.getOutcome()
        if result:
            print(result)
            break
        print(chessLogic.get_board())

    chessLogic.quitEngine()