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

@socket_io.on('new-game')
def newGame(arg):
    print(f'new to-server event: {arg}')
    chess_logic.reset_board()

@socket_io.on('start-game')
def startGame(arg):
    while chess_logic.getOutcome() is None:
        move = getStockfishMove() #! Change for user input
        if not chess_logic.validateMove(move):
            socket_io.emit('validation-error')
            continue
        move = move.uci()
        chess_logic.movePiece(move)
        if chess_logic.checkSpecialMove()[0] == "castling":
            rookMove = chess_logic.checkSpecialMove()[1]
            print("castling")
            emitMove(rookMove)
            time.sleep(1) #Sleep added because the frontend is unable to keep up with rook special move
        elif chess_logic.checkSpecialMove()[0]=="passant":
            pass
        elif chess_logic.checkSpecialMove()[0]=="promotion":
            promotion = move[-1]
            move = move[:-1]
        emitMove(move)
        if chess_logic.checkSpecialMove()[0]=="promotion":
            move = translate_notation(move)
            promo = {"promotion": promotion, "currX": move[0], "currY": move[1], "turn": chess_logic.getPlayerTurn()}
            socket_io.emit('promotion', promo)
        print(chess_logic.get_board())
    print(chess_logic.getOutcome())
    print("Result, winner is: " + chess_logic.getWinner())

def emitMove(move):
    tMove = translate_notation(move)
    msg = {"prevX": tMove[0], "prevY": tMove[1], "nextX": tMove[2], "nextY": tMove[3], 
           "checkmate": chess_logic.check_mate(), "result": chess_logic.getOutcome()}
    socket_io.emit('from-server', msg)

def getUserInput():
    move = input("Enter move: ")
    return chess.Move.from_uci(move)

def getStockfishMove():
    return chess_logic.getBestMove()

if __name__ == '__main__':
    socket_io.run(app, port=5000)
