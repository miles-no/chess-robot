from argparse import ArgumentParser
from flask import Flask
from flask_socketio import SocketIO
from config import STOCKFISH_PATH
from chessLogic.chessLogic import ChessLogic
from certaboHelper.certabo import Certabo
from initCertabo import InitializeCertabo
from database.db_func import get_leaderboard
import time

app = Flask(__name__)
socket_io = SocketIO(app, cors_allowed_origins="*")

new_game = False
chess_logic = ChessLogic(STOCKFISH_PATH)

calibrate = False 
parser = ArgumentParser()
parser.add_argument('--calibrate', action="store_true")
args = parser.parse_args()
if args.calibrate:
    calibrate = args.calibrate

InitializeCertabo()
mycertabo = Certabo(calibrate)

# SocketIO to handle new connections
# Prints for every new connection
@socket_io.on('connect')
def handle_connect():
    print('new connection')

@socket_io.on('new-game')
def newGame(arg):
    setPreferences(arg)
    message = {"fen": "start", "color": True}
    socket_io.emit("get-fen", message)
    mycertabo.new_game()
    if mycertabo.color == mycertabo.stockfish_color:
        move = handleStockfishMove()
        emitFen(move)
   
@socket_io.on('get-valid-moves')
def getValidMoves():
    legal_moves = list(mycertabo.chessboard.legal_moves)
    legal_moves_ucis = []
    for move in legal_moves:
        legal_moves_ucis.append(move.uci())
    socket_io.emit('valid-moves', legal_moves_ucis)

@socket_io.on('start-game')
def startGame(arg):
    setPreferences(arg)
    while chess_logic.getOutcome(mycertabo.chessboard) is None:
        if mycertabo.color == mycertabo.stockfish_color:
            move = handleStockfishMove()
        else:
            move = mycertabo.get_user_move()
            if move == "Invalid move":
                socket_io.emit("invalid-move")
                continue
            mycertabo.setColor()
        emitFen(move)
    outcome = chess_logic.getOutcome(mycertabo.chessboard)
    score = chess_logic.getScore(mycertabo.chessboard, mycertabo.stockfish_color)
    print("Score: ", score)
    result = {"result": outcome[0], "winner": outcome[1], "score": score}
    socket_io.emit("game-over", result)
    print("Game over")

@socket_io.on('get-leaderboard')
def getLeaderboard():
    data = get_leaderboard()
    socket_io.emit("leaderboard", data)

def setPreferences(arg):
    mycertabo.setStockfishColor(arg['color'])
    chess_logic.setSkillLevel(arg['skill_level'])

def handleStockfishMove():
    best_move = chess_logic.getBestMove(mycertabo.chessboard)
    time.sleep(2)
    mycertabo.stockfish_move(best_move)
    mycertabo.setColor()
    return best_move.uci()

def emitFen(move):
    fen = mycertabo.chessboard.board_fen()
    message = {"fen": fen, "color": mycertabo.color, 'move': move}
    socket_io.emit("get-fen", message)

if __name__ == '__main__':
    socket_io.run(app, port=5000)
