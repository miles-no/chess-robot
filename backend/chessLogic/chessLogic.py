import chess
import chess.engine

class ChessLogic:
    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/opt/stockfish/bin/stockfish")

    def getBestMove(self, board):
        result = self.engine.play(board, chess.engine.Limit(time=0.1))
        best_move = result.move
        return best_move
    
    def quitEnine(self):
        self.engine.quit()
    
    def validateMove(self, board, move):
        return move in board.legal_moves

if __name__ == "__main__":
    board = chess.Board()
    print(board)
    print(type(board))
    chessLogic = ChessLogic()
    print(chessLogic.getBestMove(board))
    chessLogic.quitEnine()