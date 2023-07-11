from flask import Flask
from flask_socketio import SocketIO
from config import STOCKFISH_PATH
from chessLogic.chessLogic import ChessLogic
from certaboHelper.certabo import Certabo
from initCertabo import InitializeCertabo

app = Flask(__name__)
socket_io = SocketIO(app, cors_allowed_origins="*")

chess_logic = ChessLogic(STOCKFISH_PATH)

InitializeCertabo()
calibrate = 2 # do fresh calibration
mycertabo = Certabo(calibrate)

# SocketIO to handle new connections
# Prints for every new connection
@socket_io.on('connect')
def handle_connect():
    print('new connection')

@socket_io.on('new-game')
def newGame(arg):
    print(f'new to-server event: {arg}')
    mycertabo.new_game()

@socket_io.on('start-game')
def startGame(arg):
    print(arg)
    while chess_logic.getOutcome(mycertabo.chessboard) is None:
        mycertabo.get_user_move()
        fen = mycertabo.chessboard.board_fen()
        socket_io.emit("get-fen", fen)
    outcome = chess_logic.getOutcome(mycertabo.chessboard)
    result = {"result": outcome[0], "winner": outcome[1]}
    socket_io.emit("game-over", result)
    print("Game over")

if __name__ == '__main__':
    socket_io.run(app, port=5000)
