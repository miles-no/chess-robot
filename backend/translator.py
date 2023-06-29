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

def translate_notation(prevState, currState):
    prevX, prevY = prevState[:len(prevState)//2].lower(), prevState[len(prevState)//2:]
    currX, currY = currState[:len(currState)//2].lower(), currState[len(currState)//2:]
    return(translator[prevX], int(prevY)-1, translator[currX], int(currY)-1)


if __name__ == "__main__":
    print(translate_notation("E2", "a2"))