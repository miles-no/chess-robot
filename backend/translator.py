translator = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7
}

def translate_notation(fen):
    prevState, currState = fen[:len(fen)//2], fen[len(fen)//2:]
    prevX, prevY = prevState[:len(prevState)//2], prevState[len(prevState)//2:]
    currX, currY = currState[:len(currState)//2], currState[len(currState)//2:]
    return(translator[prevX], int(prevY)-1, translator[currX], int(currY)-1)


if __name__ == "__main__":
    print(translate_notation("e2a2"))