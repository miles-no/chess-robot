from flask import Flask
from flask_socketio import SocketIO
import datetime
from chessLogic.translator import translate_notation
from config import STOCKFISH_PATH
from chessLogic.chessLogic import ChessLogic
import chess
import time

x = datetime.datetime.now()

app = Flask(__name__)
socket_io = SocketIO(app, cors_allowed_origins="*")

chess_logic = ChessLogic(STOCKFISH_PATH)

# SocketIO to handle new connections
# Prints for every new connection
@socket_io.on('connect')
def handle_connect():
    print('new connection')

# Will print the sent argument amd semd back the current time
@socket_io.on('to-server')
def handle_to_server(arg):
    print(f'new to-server event: {arg}')
    move = getStockfishMove() #! Change for user input
    validation = chess_logic.validateMove(move)
    if not validation:
        print("Stockfish made an illegal move")
        print("MOVE ::: " + move)
        socket_io.emit('from-server', validation)
        return
    print("Stockfish made a legal move")
    move = move.uci()
    chess_logic.movePiece(move)
    message = translate_notation(move)
    messageDictionary = {"prevX": message[0], "prevY": message[1], 
                         "nextX": message[2], "nextY": message[3], "checkmate": chess_logic.check_mate(), "result": chess_logic.getOutcome()}
    print(chess_logic.get_board())
    if(chess_logic.getOutcome()):
        print(chess_logic.getOutcome())
    socket_io.emit('from-server', messageDictionary)

@socket_io.on('new-game')
def newGame(arg):
    print(f'new to-server event: {arg}')
    chess_logic.reset_board()

@socket_io.on('start-game')
def startGame(arg):
    print(f'new to-server event: {arg}')
    while chess_logic.getOutcome() is None:
        move = getStockfishMove() #! Change for user input
        validation = chess_logic.validateMove(move)
        if not validation:
            print("Illegal move")
            socket_io.emit('from-server', validation)
            return
        print("Stockfish made a legal move")
        move = move.uci()
        chess_logic.movePiece(move)
        if chess_logic.checkSpecialMove():
            
            rookMove = chess_logic.checkSpecialMove()
            if rookMove is True:
               print("OTHER SPECIAL")
               break
            message2 = translate_notation(rookMove)
            messageDictionary2 = {"prevX": message2[0], "prevY": message2[1], 
                            "nextX": message2[2], "nextY": message2[3],
                              "checkmate": chess_logic.check_mate(), "result": chess_logic.getOutcome()}
            socket_io.emit('from-server', messageDictionary2)
            print("SPECIAL MOVE")
            print(chess_logic.get_board())
            time.sleep(1) #Sleep added because the frontend is unable to keep up with rook special move
        message = translate_notation(move)
        messageDictionary = {"prevX": message[0], "prevY": message[1], 
                            "nextX": message[2], "nextY": message[3], "checkmate": chess_logic.check_mate(), "result": chess_logic.getOutcome()}
        print(chess_logic.get_board())
        if(chess_logic.getOutcome()):
            print(chess_logic.getOutcome())
            print("Result, winner is: " + chess_logic.getWinner())
        socket_io.emit('from-server', messageDictionary)
    print("Game over")


def getUserInput():
    move = input("Enter move: ")
    return chess.Move.from_uci(move)

def getStockfishMove():
    return chess_logic.getBestMove()

if __name__ == '__main__':
    socket_io.run(app, port=5000)
