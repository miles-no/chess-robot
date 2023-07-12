import chess
import chess.engine
class ChessLogic:
    def __init__(self, STOCKFISH_PATH):
        self.last_move = None
        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        self.color = True

    def quitEngine(self):
        self.engine.quit()
    
    def setSkillLevel(self, skill_level=1):
        self.engine.configure({"Skill Level": skill_level})

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
    
    # True for white and False for black
    def setColor(self):
        if self.color: 
            self.color = False
        else:
            self.color = True
    
    def getStockfishColor(self, color):
        if color: 
            return False
        else: 
            return True

    
if __name__ == "__main__":
    pass