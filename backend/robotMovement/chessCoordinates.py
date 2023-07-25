class ChessCoordinates():
    def __init__(self):
        self.tile = 35
        self.a_position = {"x": 150, "y": 120}

    def chess_to_robot(self, position):
        y, number = self.split_strings(position)
        x = number-1
        x = self.a_position["x"] + x*self.tile
        y = self.a_position["y"] - y*self.tile
        return x, y
    
    # queen or king on the side
    def kq_on_side_lift(self, kq_position, move):
        if kq_position != None:
            for position in kq_position:
                LNking, Nking = self.split_strings(position)
                move_from, _ = move[:len(move)//2], move[len(move)//2:]
                LNfrom, Nfrom = self.split_strings(move_from)

                if Nking == Nfrom and LNking-1 == LNfrom or Nking == Nfrom and LNking+1 == LNfrom:
                    print("King or queen is on the side when picking up")
                    return True

    # queen or king on the side
    def kq_on_side_down(self, kq_position, move):
        if kq_position != None:
            for position in kq_position:
                LNking, Nking = self.split_strings(position)
                _, move_to = move[:len(move)//2], move[len(move)//2:]
                LNto, Nto = self.split_strings(move_to)

                if Nking == Nto and LNking-1 == LNto or Nking == Nto and LNking+1 == LNto:
                    print("King or queen is on the side when putting down")
                    return True
    
    def split_strings(self, string):
        letter, number = string[:len(string)//2], int(string[len(string)//2:])
        l2n = ord(letter)-97
        return l2n, number

if __name__ == "__main__":
    cc = ChessCoordinates()
    cc.get_piece_position("h1")