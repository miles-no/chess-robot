import sys
import os
import chess
import platform
import pathlib

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chessLogic.chessLogic import ChessLogic
from config import STOCKFISH_PATH

def setup_stockfish_path():
    """Set up Stockfish path similar to server.py"""
    if platform.system() == "Windows":
        loc = pathlib.Path(__file__).parent.parent.parent
        return "".join([str(loc), STOCKFISH_PATH])
    elif platform.system() == "Darwin":
        return STOCKFISH_PATH
    else:
        return ""

def test_promotion_detection():
    """Test if promotion is detected correctly"""
    
    # Initialize chess logic with Stockfish
    pStockfish = setup_stockfish_path()
    chess_logic = ChessLogic(pStockfish)
    
    print("=== Testing Promotion Detection ===\n")
    
    # Test black promotion (2nd rank to 1st rank)
    print("1. Testing black promotion (b2 → b1)...")
    board = chess.Board("8/8/8/8/8/8/1p6/8 b - - 0 1")  # Black pawn on b2
    chess_logic.chessboard = board
    
    # Make promotion move
    move = chess.Move.from_uci("b2b1q")
    board.push(move)
    
    # Check if promotion is detected
    result = chess_logic.checkPromotion()
    print(f"   Black promotion detected: {result}")
    if result:
        print("   ✅ Black promotion test PASSED")
    else:
        print("   ❌ Black promotion test FAILED")
    
    # Test white promotion (7th rank to 8th rank)
    print("\n2. Testing white promotion (b7 → b8)...")
    board = chess.Board("8/1P6/8/8/8/8/8/8 w - - 0 1")  # White pawn on b7
    chess_logic.chessboard = board
    
    # Make promotion move
    move = chess.Move.from_uci("b7b8q")
    board.push(move)
    
    # Check if promotion is detected
    result = chess_logic.checkPromotion()
    print(f"   White promotion detected: {result}")
    if result:
        print("   ✅ White promotion test PASSED")
    else:
        print("   ❌ White promotion test FAILED")
    
    # Test pieces dictionary
    print("\n3. Testing promotion pieces mapping...")
    try:
        queen_symbol = chess_logic.pieces['q']
        print(f"   Queen symbol: {queen_symbol}")
        print("   ✅ Pieces mapping test PASSED")
    except Exception as e:
        print(f"   ❌ Pieces mapping test FAILED: {e}")

def test_move_validation():
    """Test promotion move validation"""
    print("\n=== Testing Move Validation ===\n")
    
    pStockfish = setup_stockfish_path()
    chess_logic = ChessLogic(pStockfish)
    
    # Test valid promotion moves
    board = chess.Board("8/8/8/8/8/8/1p6/8 b - - 0 1")
    valid_moves = ["b2b1q", "b2b1r", "b2b1b", "b2b1n"]
    
    for move_str in valid_moves:
        move = chess.Move.from_uci(move_str)
        is_legal = move in board.legal_moves
        print(f"   Move {move_str} is legal: {is_legal}")

if __name__ == "__main__":
    test_promotion_detection()
    test_move_validation()
    print("\n=== Test Complete ===")
    print("To test with physical board:")
    print("1. Start server: python3 server.py")
    print("2. Place black pawn on b2")
    print("3. Move to b1 and watch for promotion")