import chess
import chess.engine
class ChessLogic:
    def __init__(self, STOCKFISH_PATH):
        self.board = chess.Board()
        self.last_move = None
        self.previous_move = None
        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        self.engine.configure({"Skill Level": 1})

    # Returns move in 'chess.Move' format
    def getBestMove(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=0.3))
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
        self.last_move = move
        self.board.push(move)

    def getOutcome(self, board):
    #.winner returns true for white win, false for black, None for draw
        if board.outcome():
            #Transforming outcome() to satisfactory format
            result = str(board.outcome().termination).split('.')
            result = result[1].replace('_', ' ').title()
            return result, self.getWinner(board)

    def getWinner(self, board):
        if board.outcome().winner == True:
            return "white"
        elif board.outcome().winner == False:
            return "black"
        return "undefined"

    
if __name__ == "__main__":
    pass