import { Button } from "@mui/material";
import { useEffect, useState } from "react";
import { Socket } from "socket.io-client";
import AlertComponent from "../../Components/Alert/Notification";
import MyChessboard from "../../Components/Chessboard/Chessboard";
import GameStatus from "../../Components/GameStatus/GameStatus";
import { default as PreGame } from "../../Components/PreGame/PreGame";
import "./index.css";
interface gameProps {
  socket: Socket;
}

export default function Game(props: gameProps) {
  const [FEN, setFEN] = useState<string>("start");
  const [moves, setMoves] = useState<string[]>();
  const [open, setOpen] = useState<boolean>(false);
  const [result, setResult] = useState<string>();
  const [winner, setWinner] = useState<string>();
  const [color, setColor] = useState<boolean>();
  const [preGame, setpreGame] = useState<boolean>(true);
  const [stockfishlevel, setStockfishLevel] = useState<number>(0);
  const [valid_moves, setValidMoves] = useState<string[]>();
  const [timer, setTimer] = useState<number>(0);
  const [currentPlayer, setCurrentPlayer] = useState<boolean>(true);
  const [gameInProgress, setGameInProgress] = useState<boolean>(false);

  useEffect(() => {
    props.socket.on("invalid-move", handleInvalidMove);
    props.socket.on("valid-moves", handleValidMoves);
    props.socket.on("get-fen", handleFEN);
    props.socket.on("game-over", handleResultMessage);
    return () => {
      // Cleanup the props.socket listener when the component unmounts
      props.socket.off("invalid-move", handleInvalidMove);
      props.socket.off("valid-moves", handleValidMoves);
      props.socket.off("get-fen", handleFEN);
      props.socket.off("game-over", handleResultMessage);
    };
  }, [props.socket]);

  const newGame = async () => {
    if (gameInProgress) {
      const confirmNewGame = window.confirm(
        "Are you sure you want to start a new game? Please adjust the pieces to starting positions!"
      );
      if (!confirmNewGame) {
        return; // Exit early if the user cancels the new game confirmation
      }
      setpreGame(true);
      setFEN("start");
      setGameInProgress(false);
      let piece_color;
      if (color === "white") {
        piece_color = true;
      } else {
        piece_color = false;
      }
      console.log(piece_color);
      const preferences = { skill_level: stockfishlevel, color: piece_color };
      props.socket.emit("new-game", preferences);
    }
  };
  const handleFEN = (message: any) => {
    if (message.fen) {
      setFEN(message.fen);
      setValidMoves([]);
      setCurrentPlayer(message.color);
      setMoves(message.move);
      console.log("COLOR: " + message.color);
    }
  };

  function startGame() {
    if (FEN === "start" && props.socket.connected) {
      const preferences = { skill_level: stockfishlevel, color: color };
      props.socket.emit("start-game", preferences);
      setGameInProgress(true);
    } else {
      setOpen(true);
    }
  }

  function handleResultMessage(messageDisctionary: any) {
    if (messageDisctionary.result) {
      setResult(messageDisctionary.result);
      setOpen(true);
      setGameInProgress(false);
    }
    if (messageDisctionary.winner) {
      setWinner(messageDisctionary.winner);
    }
  }

  const handleInvalidMove = () => {
    alert("Invalid move!");
  };

  const handleClose = () => {
    // On closing the alert
    setOpen(false);
  };

  const handleOK = () => {
    setResult(undefined);
    setOpen(false);
    newGame();
  };

  const handlePregame = (level: number, selectedSide: boolean) => {
    setStockfishLevel(level);
    setColor(selectedSide);
    setpreGame(false);
  };

  const getValidMoves = () => {
    props.socket.emit("get-valid-moves");
  };

  const handleValidMoves = (validMoves: string[]) => {
    setValidMoves(validMoves);
  };

  return (
    <div>
      {preGame ? (
        <div className="pre-game">
          <PreGame
            open={preGame}
            stockfishLevel={stockfishlevel}
            handleOK={handlePregame}
          />
        </div>
      ) : (
        <div className="main-container">
          <div className="game">
            <div className="alert">
              {result && (
                <AlertComponent
                  open={open}
                  alertTitle={result}
                  message={"Winner is " + winner}
                  handleClose={handleClose}
                  handleOK={handleOK}
                />
              )}
            </div>
            <div className="unclickable-area">
              <MyChessboard boardWidth={600} socket={props.socket} FEN={FEN} />
            </div>
            {!result && (
              <AlertComponent
                alertTitle="Start Game"
                message="Make sure pieces are in starting position"
                handleClose={handleClose}
                handleOK={handleOK}
                open={open}
              />
            )}
            <div className="buttons">
              {gameInProgress ? (
                <>
                  <Button variant="outlined" onClick={() => newGame()}>
                    New game
                  </Button>
                  <Button variant="outlined" onClick={() => getValidMoves()}>
                    Get move
                  </Button>
                </>
              ) : (
                !gameInProgress && (
                  <Button variant="contained" onClick={() => startGame()}>
                    Start game
                  </Button>
                )
              )}
            </div>
            <div>{valid_moves && valid_moves.map((move) => <p>{move}</p>)}</div>
          </div>
          <div className="game-status">
            {gameInProgress && (
              <GameStatus moves={moves} player={currentPlayer} />
            )}
          </div>
        </div>
      )}
    </div>
  );
}
