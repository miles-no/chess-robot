from flask import Flask
from flask_socketio import SocketIO
import datetime
from config import STOCKFISH_PATH
from chessLogic.chessLogic import ChessLogic
from test_certabo import mycertabo

x = datetime.datetime.now()

app = Flask(__name__)
socket_io = SocketIO(app, cors_allowed_origins="*")

chess_logic = ChessLogic(STOCKFISH_PATH)

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
    for i in range(40):
        print("READY")
        print(mycertabo.get_user_move())
        move = mycertabo.pending_moves[0]
        fen = mycertabo.chessboard.board_fen()
        print(fen)
        print(move)

    print("Game over")
if __name__ == '__main__':
    socket_io.run(app, port=5000)
