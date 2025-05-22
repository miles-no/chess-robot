from argparse import ArgumentParser
import pathlib
from flask import Flask
from flask_socketio import SocketIO
from chessLogic.chessLogic import ChessLogic
from certaboHelper.certabo import Certabo
from certaboHelper.initCertabo import InitializeCertabo
from database.db_func import get_leaderboard, add_player
from robotMovement.chessRobot import ChessRobot
import time
import platform
from datetime import datetime
import os
from pathlib import Path


app = Flask(__name__)
socket_io = SocketIO(app, cors_allowed_origins="*")

pStockfish = ""
if platform.system() == 'Windows':
    # Stockfish executable expected in chess-robot folder 
     loc = pathlib.Path(__file__).parent.parent
     conf = ''.join([str(loc),STOCKFISH_PATH])
     pStockfish = conf
elif platform.system() == 'Darwin': #Darwin for MacOS
    pStockfish = "/opt/homebrew/bin/stockfish"
else: #Default to Linux
    pStockfish ="/usr/local/bin/stockfish"

chess_logic = ChessLogic(pStockfish)

InitializeCertabo()
mycertabo = Certabo()

try:
    cr = ChessRobot()
    if cr.arm is None:
        print("Warning: xArm not initialized. Robot movements will be simulated.")
except Exception as e:
    print(f"Error initializing ChessRobot: {e}")
    cr = None

# SocketIO to handle new connections
# Prints for every new connection
@socket_io.on('connect')
def handle_connect():
    print("New connection")

@socket_io.on('new-game')
def newGame(arg):
    mycertabo.moves = []
    mycertabo.new_game()
    cr.reset_taken()
    emitFen()
    startGame(arg)
    emitAnalysis()

@socket_io.on('stop-game')
def stopGame():
    chess_logic.game_status = False
   
@socket_io.on('get-valid-moves')
def getValidMoves():
    legal_moves = list(mycertabo.chessboard.legal_moves)
    if len(legal_moves) == 0:
        socket_io.emit('valid-moves', [])
        return
    best_move = chess_logic.getBestMove(mycertabo.chessboard)
    legal_moves_ucis = [best_move.uci()]
    for move in legal_moves:
        if best_move != move:
            legal_moves_ucis.append(move.uci())
    chess_logic.reduction += 100
    socket_io.emit('valid-moves', legal_moves_ucis)

@socket_io.on('start-game')
def startGame(arg):
    setPreferences(arg)
    chess_logic.game_status = True
    while chess_logic.getOutcome(mycertabo.chessboard) is None:
        if not chess_logic.game_status:
            break
        if mycertabo.color == mycertabo.stockfish_color:
            move = handleStockfishMove()
        else:
            move = mycertabo.get_user_move()
            if move[1] == "Invalid move":
                if chess_logic.game_status:
                    socket_io.emit("invalid-move")
                    continue
                else:
                    break
            mycertabo.setColor()
            move = move[0]
        doMove(move)
    outcome = chess_logic.getOutcome(mycertabo.chessboard)
    if outcome != None:
        score = chess_logic.getScore(mycertabo.chessboard, mycertabo.stockfish_color)
        print("Score: ", score)
        result = {"result": outcome[0], "winner": outcome[1], "score": score}
        socket_io.emit("game-over", result)
        add_player(chess_logic.player, score, datetime.now().strftime("%d/%m/%Y %H:%M"), chess_logic.skill_level)
        print("Game over")
        chess_logic.game_status = False

@socket_io.on('get-leaderboard')
def getLeaderboard():
    data = get_leaderboard()
    socket_io.emit("leaderboard", data)

def setPreferences(arg):
    mycertabo.setStockfishColor(arg['color'])
    chess_logic.setSkillLevel(arg['skill_level'])
    chess_logic.setPlayer(arg['name'])

def handleStockfishMove():
    best_move = chess_logic.getBestMove(mycertabo.chessboard)
    time.sleep(2)
    # Check passant
    if chess_logic.checkPassant(best_move, mycertabo.chessboard):
        piece_to_remove = best_move.uci()[2]+best_move.uci()[1]
        cr.move_taken(piece_to_remove, "p",  mycertabo.stockfish_color)
    # Check if piece is taken
    elif mycertabo.chessboard.is_capture(best_move):
        cr.move_taken(best_move.uci()[2:], str(mycertabo.chessboard.piece_at(best_move.to_square)).lower(),  mycertabo.stockfish_color)

    mycertabo.stockfish_move(best_move)
    best_move = best_move.uci()

    # Check promotion
    if chess_logic.checkPromotion():
        promotion = chess_logic.pieces[best_move[-1]]
        best_move = best_move[:-1]
        prom_move = best_move[:len(best_move)//2]
        cr.move_taken(prom_move, "p",  mycertabo.stockfish_color)
        socket_io.emit("promotion", promotion)
    else:
        # Check castling
        castling = chess_logic.checkCastling()
        if castling:
            cr.doMove(castling, mycertabo.stockfish_color)    
        cr.doMove(best_move,  mycertabo.stockfish_color)
    cr.reset()
    mycertabo.setColor()
    return best_move

def doMove(move):
    mycertabo.moves.append(move)
    emitFen()
    emitAnalysis()

def emitFen():
    fen = mycertabo.chessboard.board_fen()
    message = {"fen": fen, "color": mycertabo.color, 'moves': mycertabo.moves}
    socket_io.emit("get-fen", message)

def emitAnalysis():
    analysis = chess_logic.getBoardAnalysis(mycertabo.chessboard)
    socket_io.emit("analysis", { "relativeScore": analysis })

if __name__ == '__main__':
    socket_io.run(app, port=5000)
