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
        playerTurn = chess_logic.getPlayerTurn()
        move = getStockfishMove() #! Change for user input
        if not chess_logic.validateMove(move):
            socket_io.emit('validation-error')
            continue
        if chess_logic.checkPassant(move):
            tmove = translate_notation(move.uci())
            passant = {"currX": tmove[2], "currY": tmove[1]}
            socket_io.emit('passant', passant)
        move = move.uci()
        chess_logic.movePiece(move)
        if chess_logic.checkCastling():
            rookMove = chess_logic.checkCastling()
            emitMove(rookMove)
            time.sleep(1) #Sleep added because the frontend is unable to keep up with rook special move
        elif chess_logic.checkPromotion():
            promotion = move[-1]
            move = move[:-1]
            pmove = translate_notation(move)
            promo = {"promotion": promotion, "currX": pmove[0], "currY": pmove[1], "turn": playerTurn}
            socket_io.emit('promotion', promo)
        emitMove(move)
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


# PASSANT_TEST = ["f2f3", "b7b5", "g2g4", "b5b4", "a2a4", "b4a3", "h2h4", "h7h6"]
# PROMOTION_TEST = ["a2a4", "b7b5", "a4b5", "b8c6", "a1a5", "c6a5", "b5b6", "a5b3", "b6b7", "b3a1", "b7b8r", "g7g5"]

# @socket_io.on('start-game')
# def startGame(arg):
#     for i in range(len(PROMOTION_TEST)-1):
#         playerTurn = chess_logic.getPlayerTurn()
#         move = PROMOTION_TEST[i]
#         move = chess.Move.from_uci(move)
#         if not chess_logic.validateMove(move):
#             socket_io.emit('validation-error')
#             continue
#         if chess_logic.checkPassant(move):
#             tmove = translate_notation(move.uci())
#             passant = {"currX": tmove[2], "currY": tmove[1]}
#             socket_io.emit('passant', passant)
#             print("Passant")
#         move = move.uci()
#         chess_logic.movePiece(move)
#         if chess_logic.checkSpecialMove():
#             rookMove = chess_logic.checkSpecialMove()
#             print("castling")
#             emitMove(rookMove)
#             time.sleep(1) #Sleep added because the frontend is unable to keep up with rook special move
#         elif chess_logic.checkPromotion():
#             promotion = move[-1]
#             move = move[:-1]
#             print("SECOND IF")
#             pmove = translate_notation(move)
#             promo = {"promotion": promotion, "currX": pmove[0], "currY": pmove[1], "turn": playerTurn}
#             socket_io.emit('promotion', promo)
#         emitMove(move)
#         print(chess_logic.get_board())
#         time.sleep(1)
#     print("Game over")


# @socket_io.on('start-game')
# def testPassant(arg):
#     for i in range(len(PASSANT_TEST)-1):
#         print("Can I do passant?")
#         print(chess_logic.get_board().has_legal_en_passant())
#         move = PASSANT_TEST[i]
#         move = chess.Move.from_uci(move)
#         if not chess_logic.validateMove(move):
#             socket_io.emit('validation-error')
#             continue
#         if chess_logic.checkPassant(move):
#             tmove = translate_notation(move.uci())
#             passant = {"currX": tmove[2], "currY": tmove[1]}
#             socket_io.emit('passant', passant)
#             print("Passant")
#         move = move.uci()
#         chess_logic.movePiece(move)
#         if chess_logic.checkSpecialMove()[0] == "castling":
#             rookMove = chess_logic.checkSpecialMove()[1]
#             print("castling")
#             emitMove(rookMove)
#             time.sleep(1) #Sleep added because the frontend is unable to keep up with rook special move
#         elif chess_logic.checkSpecialMove()[0]=="promotion":
#             promotion = move[-1]
#             move = move[:-1]
#         emitMove(move)
#         if chess_logic.checkSpecialMove()[0]=="promotion":
#             move = translate_notation(move)
#             promo = {"promotion": promotion, "currX": move[0], "currY": move[1], "turn": chess_logic.getPlayerTurn()}
#             socket_io.emit('promotion', promo)
#         print(chess_logic.get_board())
#         time.sleep(1)
#     print("Game over")

if __name__ == '__main__':
    socket_io.run(app, port=5000)
