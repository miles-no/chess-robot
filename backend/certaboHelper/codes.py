from __future__ import print_function
import pickle
import chess
import logging

# data conversion
p, r, n, b, k, q, P, R, N, B, K, Q = [], [], [], [], [], [], [], [], [], [], [], []

# for calibration
def cell_codes(n_cell, usb_data):  # n_cell from 0 to 63, 0 at left top
    result = []
    for i in range(5):
        result.append(usb_data[n_cell * 5 + i])
    return result

def compare_cells(x, y):
    if x[0] == y[0] and x[1] == y[1] and x[2] == y[2] and x[3] == y[3] and x[4] == y[4]:
        return True
    return False

def load_calibration(filename):
    global p, r, n, b, k, q, P, R, N, B, K, Q
    logging.info("codes.py - loading calibration")
    try:
        p, r, n, b, k, q, P, R, N, B, K, Q = pickle.load(
            open(filename, "rb")
        )
    except (IOError, OSError):
        logging.info("WARNING: no calibration found")
        return False
    except ValueError:
        logging.info("Can't load calibration data")
        return False
    return True

def statistic_processing_for_calibration(samples):
    global letters
    result = []
    for n_cell in range(64):
        cells = []
        for usb_data in samples:
            cells.append(cell_codes(n_cell, usb_data))
        histograms = []
        for cell in cells:
            histogram = 0
            for c in cells:
                if compare_cells(cell, c):
                    histogram += 1
            histograms.append(histogram)
        max_value = max(histograms)
        max_index = histograms.index(max_value)
        for i in cells[max_index]:
            result.append(i)
    return result

def get_name(cell):
    global p, r, n, b, k, q, P, R, N, B, K, Q
    c = ""
    if cell_empty(cell):
        c = "-"
    for cell_p in p:
        if compare_cells(cell, cell_p):
            c = "p"
    for cell_p in P:
        if compare_cells(cell, cell_p):
            c = "P"
    for cell_p in r:
        if compare_cells(cell, cell_p):
            c = "r"
    for cell_p in R:
        if compare_cells(cell, cell_p):
            c = "R"
    for cell_p in n:
        if compare_cells(cell, cell_p):
            c = "n"
    for cell_p in N:
        if compare_cells(cell, cell_p):
            c = "N"
    for cell_p in b:
        if compare_cells(cell, cell_p):
            c = "b"
    for cell_p in B:
        if compare_cells(cell, cell_p):
            c = "B"
    for cell_p in q:
        if compare_cells(cell, cell_p):
            c = "q"
    for cell_p in Q:
        if compare_cells(cell, cell_p):
            c = "Q"
    for cell_p in k:
        if compare_cells(cell, cell_p):
            c = "k"
    for cell_p in K:
        if compare_cells(cell, cell_p):
            c = "K"
    return c


def statistic_processing(samples):
    global letters
    result = []
    found_unknown_cell = False
    for n_cell in range(64):
        cells = []
        for usb_data in samples:
            cells.append(cell_codes(n_cell, usb_data))
        histograms = []
        known_cells = []
        for cell in cells:  # stack of history of cell codes for one cell
            name = get_name(cell)
            if name != "":
                known_cells.append(cell)
            elif name == "-":           
                cell = 0, 0, 0, 0, 0
            else:            	
               	cell = 0, 0, 0, 0, 0            	    
                known_cells.append(cell)	
        if len(known_cells) == 0:
            logging.info(
                "Found only unknown cell codes in cell %s:",
                letter[n_cell % 8] + str(8 - n_cell / 8),
            )
            for cell in cells:  # stack of history of cell codes for one cell
                logging.info("%s", cell)

            found_unknown_cell = True
            break

        for cell in known_cells:  # stack of history of cell codes for one cell
            histogram = 0
            for c in cells:
                if compare_cells(cell, c):
                    histogram += 1
            histograms.append(histogram)

        max_value = max(histograms)
        max_index = histograms.index(max_value)

        # append cells[max_index] to result
        for i in known_cells[max_index]:
            result.append(i)
    if found_unknown_cell:
        return []
    return result


# ---------------------------
def cell_empty(x):
    nzeros = 0
    for n in x:
        if n == 0:
            nzeros += 1
    if nzeros > 2:
        return True
    return False


def calibration(usb_data, filename):
    global p, r, n, b, k, q, P, R, N, B, K, Q
    prev_results = p, r, n, b, k, q, P, R, N, B, K, Q

    p, r, n, b, k, q, P, R, N, B, K, Q = [], [], [], [], [], [], [], [], [], [], [], []
    empty_cell = [0, 0, 0, 0, 0]
    # pawns
    for i in range(8):  # each place at board
        cell = cell_codes(8 + i, usb_data)
        if not compare_cells(cell, empty_cell):
            p.append(cell_codes(8 + i, usb_data))
        cell = cell_codes(48 + i, usb_data)
        if not cell_empty(cell):  # not empty
            P.append(cell_codes(48 + i, usb_data))

    r.append(cell_codes(0, usb_data))
    r.append(cell_codes(7, usb_data))
    R.append(cell_codes(56, usb_data))
    R.append(cell_codes(63, usb_data))

    n.append(cell_codes(1, usb_data))
    n.append(cell_codes(6, usb_data))
    N.append(cell_codes(57, usb_data))
    N.append(cell_codes(62, usb_data))

    b.append(cell_codes(2, usb_data))
    b.append(cell_codes(5, usb_data))
    B.append(cell_codes(58, usb_data))
    B.append(cell_codes(61, usb_data))

    q.append(cell_codes(3, usb_data))
    Q.append(cell_codes(59, usb_data))

    k.append(cell_codes(4, usb_data))
    K.append(cell_codes(60, usb_data))

    pp, rp, np, bp, kp, qp, Pp, Rp, Np, Bp, Kp, Qp = prev_results
    results = p, r, n, b, k, q, P, R, N, B, K, Q

    pn, rn, nn, bn, kn, qn, Pn, Rn, Nn, Bn, Kn, Qn = (
        p[:],
        r[:],
        n[:],
        b[:],
        k[:],
        q[:],
        P[:],
        R[:],
        N[:],
        B[:],
        K[:],
        Q[:],
    )

    def add_new(pnew, pcurrent, pprevious):
        for previous in pprevious:
            previous_not_in_current = True
            for current in pcurrent:
                if compare_cells(current, previous):
                    previous_not_in_current = False
                    break
            if previous_not_in_current:
                logging.info("previous not in current")
                pnew.append(previous)
            else:
                logging.info("previous in current")
        return pnew

    logging.info("Q before = %s", Qn)

    pn = add_new(pn, p, pp)
    rn = add_new(rn, r, rp)
    nn = add_new(nn, n, np)
    bn = add_new(bn, b, bp)
    kn = add_new(kn, k, kp)
    qn = add_new(qn, q, qp)
    Pn = add_new(Pn, P, Pp)
    Rn = add_new(Rn, R, Rp)
    Nn = add_new(Nn, N, Np)
    Bn = add_new(Bn, B, Bp)
    Kn = add_new(Kn, K, Kp)
    Qn = add_new(Qn, Q, Qp)
    logging.info("Q after = %s", Qn)

    pickle.dump(results, open(filename, "wb"))

    logging.info("----------------")

    for j in range(8):
        row = []
        for i in range(8):
            cell = cell_codes(i + j * 8, usb_data)
            if cell_empty(cell):
                row.append("-")
            else:  # not empty
                for cell_p in p:
                    if compare_cells(cell, cell_p):
                        row.append("p")
                for cell_p in P:
                    if compare_cells(cell, cell_p):
                        row.append("P")
                for cell_p in r:
                    if compare_cells(cell, cell_p):
                        row.append("r")
                for cell_p in R:
                    if compare_cells(cell, cell_p):
                        row.append("R")
                for cell_p in n:
                    if compare_cells(cell, cell_p):
                        row.append("n")
                for cell_p in N:
                    if compare_cells(cell, cell_p):
                        row.append("N")
                for cell_p in b:
                    if compare_cells(cell, cell_p):
                        row.append("b")
                for cell_p in B:
                    if compare_cells(cell, cell_p):
                        row.append("B")
                for cell_p in q:
                    if compare_cells(cell, cell_p):
                        row.append("q")
                for cell_p in Q:
                    if compare_cells(cell, cell_p):
                        row.append("Q")
                for cell_p in k:
                    if compare_cells(cell, cell_p):
                        row.append("k")
                for cell_p in K:
                    if compare_cells(cell, cell_p):
                        row.append("K")
        logging.info(" ".join(row))

letter = "a", "b", "c", "d", "e", "f", "g", "h"
reversed_letter = tuple(reversed(letter))

def diff2squareset(s1, s2):
    board1 = chess.BaseBoard(s1)
    board2 = chess.BaseBoard(s2)
    diffmap = chess.SquareSet()
    for x in range(chess.A1, chess.H8+1):
        if board1.piece_at(x) != board2.piece_at(x):
            diffmap.add(x)
    return diffmap

def squareset2ledbytes(squareset):
    return int(squareset).to_bytes(8, byteorder="big", signed=False)

def usb_data_to_FEN(usb_data):
    global letter
    s = ""
    was_unknown_piece = False
    for j in range(8):
        c = ""
        empty_cells_counter = 0
        for i in range(8):
            cell = cell_codes(i + j * 8, usb_data)
            c = "unknown"
            if cell_empty(cell):
                c = "-"
                empty_cells_counter += 1
            else:  # not empty
                for cell_p in p:
                    if compare_cells(cell, cell_p):
                        c = "p"
                for cell_p in P:
                    if compare_cells(cell, cell_p):
                        c = "P"
                for cell_p in r:
                    if compare_cells(cell, cell_p):
                        c = "r"
                for cell_p in R:
                    if compare_cells(cell, cell_p):
                        c = "R"
                for cell_p in n:
                    if compare_cells(cell, cell_p):
                        c = "n"
                for cell_p in N:
                    if compare_cells(cell, cell_p):
                        c = "N"
                for cell_p in b:
                    if compare_cells(cell, cell_p):
                        c = "b"
                for cell_p in B:
                    if compare_cells(cell, cell_p):
                        c = "B"
                for cell_p in q:
                    if compare_cells(cell, cell_p):
                        c = "q"
                for cell_p in Q:
                    if compare_cells(cell, cell_p):
                        c = "Q"
                for cell_p in k:
                    if compare_cells(cell, cell_p):
                        c = "k"
                for cell_p in K:
                    if compare_cells(cell, cell_p):
                        c = "K"
                if empty_cells_counter > 0 and c != "-":
                    s += str(empty_cells_counter)
                    empty_cells_counter = 0
                    s += c
                elif empty_cells_counter == 0 and c != "-":
                    s += c
                if c == "unknown":
                    logging.info("Unknown piece at %s", letter[i] + str(8 - j))
                    was_unknown_piece = True
        if empty_cells_counter > 0 and c == "-":
            s += str(empty_cells_counter)
            empty_cells_counter = 0
        if j != 7:
            s += r"/"
    s += " w KQkq - 0 1"
    if was_unknown_piece:
        return ""
    return s

black_pieces = "r", "b", "k", "n", "p", "q"
white_pieces = "R", "B", "K", "N", "P", "Q"

class NoMove(Exception):
    pass

# Get users move from FEN
def get_moves(board, fen, color):
    board_fen = fen.split()[0]
    if board.board_fen() == board_fen:
        return None
    copy_board = board.copy()
    moves = list(board.generate_legal_moves())
    for move in moves:
        copy_board.push(move)
        if board_fen == copy_board.board_fen():
            logging.debug('Single move detected - {}'.format(move.uci()))
            return move.uci()
        copy_board.pop()
    else:
        move = FEN2Move(board, chess.Board(fen), color)
        if move != "" and chess.Move.from_uci(move) not in board.legal_moves:
            return "Invalid move"
    logging.debug('Unable to detect moves')
    raise NoMove()

# Find the move that was made in string from FEN
def FEN2Move(board, new_board, white):
    nums = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}
    board = str(board).split("\n")
    new_board = str(new_board).split("\n")
    move = ""
    flip = False
    rows = range(8) if white else range(8)[::-1]
    cols = range(15) if white else range(15)[::-1]
    for i in rows:
        for x in cols:
            if board[i][x] != new_board[i][x]:
                if board[i][x] == "." and move == "":
                    flip = True
                move += str(nums.get(round(x / 2) + 1)) + str(9 - (i + 1))
    if flip:
        move = move[2] + move[3] + move[0] + move[1]
    return move