#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020 by Harald Klein <hari@vt100.at> - All rights reserved
# 
import os
import time
import logging
import logging.handlers
import appdirs
import chess.pgn
import chess

from certaboHelper.codes import *
from certaboHelper.serialreader import *

CERTABO_DATA_PATH = appdirs.user_data_dir("GUI", "Certabo")
CALIBRATION_DATA = os.path.join(CERTABO_DATA_PATH,"calibration.bin")
os.makedirs(CERTABO_DATA_PATH, exist_ok=True)

class Certabo():
    def __init__(self, calibrate=False, **kwargs):
        super().__init__(**kwargs)
        self.calibration = True if calibrate else False
        self.chessboard = chess.Board(chess.STARTING_FEN)
        self.board_state_usb = ""
        self.move_event = threading.Event()
        self.wait_for_move = False
        self.pending_move = None
        self.color = True # white pieces start
        self.stockfish_color = None

        # internal values for CERTABO board
        self.calibration_samples_counter = 0
        self.calibration_samples = []
        self.usb_data_history_depth = 3
        self.usb_data_history = list(range(self.usb_data_history_depth))
        self.usb_data_history_filled = False
        self.usb_data_history_i = 0

        # try to load calibration data (mapping of RFID chip IDs to pieces)
        load_calibration(CALIBRATION_DATA)

        # spawn a serial thread and pass our data handler
        self.serialthread = serialreader(self.handle_usb_data)
        self.serialthread.daemon = True
        self.serialthread.start()
        time.sleep(5)

    def get_user_move(self):
        self.wait_for_move = True
        logging.debug('waiting for event signal')
        self.move_event.wait()
        self.move_event.clear()
        logging.debug(f'event signal received, pending moves: {self.pending_move}')
        self.wait_for_move = False
        return self.pending_move
    
    def new_game(self):
        self.chessboard = chess.Board()
        self.color = True

    def send_leds(self, message:bytes=(0).to_bytes(8,byteorder='big',signed=False)):
        self.serialthread.send_led(message)

    def diff_leds(self):
        s1 = self.chessboard.board_fen()
        s2 = self.board_state_usb.split(" ")[0]
        if (s1 != s2):
            diffmap = diff2squareset(s1, s2)
            self.send_leds(squareset2ledbytes(diffmap))
        else:
            self.send_leds()

    def handle_usb_data(self, data):
        usb_data = list(map(int, data.split(" ")))
        if self.calibration == True:
            self.calibrate_from_usb_data(usb_data)
        else:
            if self.usb_data_history_i >= self.usb_data_history_depth:
                self.usb_data_history_filled = True
                self.usb_data_history_i = 0
            self.usb_data_history[self.usb_data_history_i] = list(usb_data)[:]
            self.usb_data_history_i += 1
            if self.usb_data_history_filled:
                self.usb_data_processed = statistic_processing(self.usb_data_history)
                if self.usb_data_processed != []:
                    test_state = usb_data_to_FEN(self.usb_data_processed)
                    if test_state != "":
                        new_position = True if self.board_state_usb != test_state else False
                        self.board_state_usb = test_state
                        self.diff_leds()
                        if new_position:
                            # new board state via usb
                            if self.wait_for_move:
                                logging.debug('trying to find user move in usb data')
                                try:
                                    self.pending_move = get_moves(self.chessboard, self.board_state_usb, self.color) # only search one move deep
                                    if self.pending_move != None and self.pending_move != "Invalid move":
                                        logging.debug('firing event')
                                        self.chessboard.push_uci(self.pending_move)
                                        self.move_event.set()
                                    elif self.pending_move == "Invalid move":
                                        self.move_event.set()
                                except NoMove:
                                    self.pending_move = None

    def calibrate_from_usb_data(self, usb_data):
        self.calibration_samples.append(usb_data)
        logging.info("    adding new calibration sample")
        self.calibration_samples_counter += 1
        if self.calibration_samples_counter >= 15:
            logging.info( "------- we have collected enough samples for averaging ----")
            usb_data = statistic_processing_for_calibration(self.calibration_samples)
            calibration(usb_data, CALIBRATION_DATA)
            self.calibration = False
            logging.info('calibration ok') 
            self.send_leds()
        elif self.calibration_samples_counter %2:
            self.send_leds(b'\xff\xff\x00\x00\x00\x00\xff\xff')
        else:
            self.send_leds()

    def stockfish_move(self, best_move):
        self.chessboard.push(best_move)

    def setColor(self):
        self.color = not self.color
    
    def setStockfishColor(self, color):
        self.stockfish_color = False if color else True

    def get_qk_positions(self):
        positions = []
        for square in self.chessboard.pieces(chess.QUEEN, chess.WHITE):
            positions.append(chess.square_name(square))
        for square in self.chessboard.pieces(chess.QUEEN, chess.BLACK):
            positions.append(chess.square_name(square))
        positions.append(chess.square_name(self.chessboard.king(chess.WHITE)))
        positions.append(chess.square_name(self.chessboard.king(chess.BLACK)))
        return positions