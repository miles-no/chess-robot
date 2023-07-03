from flask import Flask
from flask_socketio import SocketIO
import datetime
from translator import translate_notation
from chessLogic.chess import ChessLogic
import chess

x = datetime.datetime.now()

app = Flask(__name__)
socket_io = SocketIO(app, cors_allowed_origins="*")

chess_logic = ChessLogic()

# SocketIO to handle new connections
# Prints for every new connection
@socket_io.on('connect')
def handle_connect():
    print('new connection')

# Will print the sent argument amd semd back the current time
@socket_io.on('to-server')
def handle_to_server(arg):
    print(f'new to-server event: {arg}')
    message = getStockfishMove() #! Change for user input
    messageDictionary = {"prevX": message[0], "prevY": message[1], "nextX": message[2], "nextY": message[3]}
    socket_io.emit('from-server', messageDictionary)


def getUserInput():
    move = input("Enter move: ")
    return translate_notation(move)


def getStockfishMove():
    board = chess.Board()
    move = chess_logic.getBestMove(board)
    message = translate_notation(move.uci())
    return message

if __name__ == '__main__':
    socket_io.run(app, port=5000)
