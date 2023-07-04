from flask import Flask
from flask_socketio import SocketIO
import datetime
from translator import translate_notation
from chessLogic.chessLogic import ChessLogic
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
    move = getUserInput() #! Change for user input
    validation = chess_logic.validateMove(move)
    if not validation:
        print("Stockfish made an illegal move")
        socket_io.emit('from-server', validation)
        return
    print("Stockfish made a legal move")
    move = move.uci()
    chess_logic.movePiece(move)
    message = translate_notation(move)
    messageDictionary = {"prevX": message[0], "prevY": message[1], "nextX": message[2], "nextY": message[3]}
    socket_io.emit('from-server', messageDictionary)

@socket_io.on('new-game')
def handle_to_server(arg):
    print(f'new to-server event: {arg}')
    chess_logic.reset_board()

def getUserInput():
    move = input("Enter move: ")
    return chess.Move.from_uci(move)

def getStockfishMove():
    return chess_logic.getBestMove()

if __name__ == '__main__':
    socket_io.run(app, port=5000)
