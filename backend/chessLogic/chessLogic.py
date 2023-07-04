import chess
import chess.engine

class ChessLogic:
    def __init__(self):
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/opt/stockfish/bin/stockfish")

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
        self.board.push(move)
        # return board
    
    def get_board(self):
        return self.board
    
    def reset_board(self):
        self.board = chess.Board()

if __name__ == "__main__":
    chessLogic = ChessLogic()
    for i in range(5):
        print(chessLogic.get_board())
        move = str(chessLogic.getBestMove())
        print(move)
        chessLogic.movePiece(move)
        print(chessLogic.get_board())
    chessLogic.reset_board()
    print(chessLogic.get_board())
    chessLogic.quitEngine()