import chess
import chess.engine
class ChessLogic:
    def __init__(self, STOCKFISH_PATH):
        self.last_move = None
        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        self.skill_level = 1
        self.piece_range = {
            1: 1, #pawn
            2: 3, #knight
            3: 3, #bishop
            4: 5, #rook
            5: 9 #queen
        }

    def quitEngine(self):
        self.engine.quit()
    
    def setSkillLevel(self, skill_level):
        self.engine.configure({"Skill Level": skill_level})
        self.skill_level = skill_level

    # Returns move in 'chess.Move' format
    def getBestMove(self, board):
        result = self.engine.play(board, chess.engine.Limit(time=0.3))
        best_move = result.move
        return best_move
    
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
        return None
    
    def getScore(self, board, stockfish):
        if board.outcome().winner == stockfish:
            return 0
        score = 0
        for piece in self.piece_range:
            score += len(board.pieces(piece, board.outcome().winner))*self.piece_range[piece]
        return score*100/self.skill_level

    
if __name__ == "__main__":
    STOCKFISH_PATH = "/opt/homebrew/opt/stockfish/bin/stockfish"
    chess_logic = ChessLogic(STOCKFISH_PATH)
    score = chess_logic.getScore(chess.Board(), True)
    print(score)