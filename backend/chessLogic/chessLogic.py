import chess
import chess.engine

class ChessLogic:
    def __init__(self, STOCKFISH_PATH):
        self.board = chess.Board()
        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

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

if __name__ == "__main__":
    STOCKFISH_PATH = "/opt/homebrew/opt/stockfish/bin/stockfish"
    chessLogic = ChessLogic(STOCKFISH_PATH)
    while True:
        print(chessLogic.get_board())
        move = str(chessLogic.getBestMove())
        print(move)
        chessLogic.movePiece(move)
        result = chessLogic.getOutcome()
        if result:
            print(chessLogic.getOutcome())
            break
        print(chessLogic.get_board())
    print(chessLogic.getOutcome())

    chessLogic.quitEngine()