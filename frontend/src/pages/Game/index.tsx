import { Button, LinearProgress } from "@mui/material";
import { useEffect, useState } from "react";
import { Socket } from "socket.io-client";
import AlertComponent from "../../Components/Alert/Notification";
import MyChessboard from "../../Components/Chessboard/Chessboard";
import { default as PreGame } from "../../Components/PreGame/PreGame";
import "./index.css";
interface gameProps {
  socket: Socket;
}

export default function Game(props: gameProps) {
  const [FEN, setFEN] = useState<string>("start");
  const [open, setOpen] = useState<boolean>(false);
  const [result, setResult] = useState<string>();
  const [winner, setWinner] = useState<string>();
  const [color, setColor] = useState<string>();
  const [preGame, setpreGame] = useState<boolean>(true);
  const [stockfishlevel, setStockfishLevel] = useState<number>(0);
  const [valid_moves, setValidMoves] = useState<string[]>();
  useEffect(() => {
    props.socket.on("game-over", handleResultMessage);

    // Clean up the event listener on component unmount
    return () => {
      props.socket.off("game-over", handleResultMessage);
    };
  }, [props.socket]);

  useEffect(() => {
    props.socket.on("get-fen", handleFEN);
    // Cleanup the props.socket listener when the component unmounts
    return () => {
      props.socket.off("get-fen", handleFEN);
    };
  }, [props.socket]);

  useEffect(() => {
    props.socket.on("invalid-move", handleInvalidMove);
    props.socket.on("valid-moves", handleValidMoves);
    return () => {
      props.socket.off("invalid-move", handleInvalidMove);
      props.socket.off("valid-moves", handleValidMoves);
    };
  }, []);

  function newGame() {
    if (FEN !== "start") {
      const confirmNewGame = window.confirm(
        "Are you sure you want to start a new game? Please adjust the pieces to starting positions!"
      );
      if (!confirmNewGame) {
        return; // Exit early if the user cancels the new game confirmation
      }
      props.socket.emit("new-game", "new-game");
      setFEN("start");
      setpreGame(true);
    }
  }
  const handleFEN = (fen: string) => {
    if (fen) {
      setFEN(fen);
      setValidMoves([]);
    }
  };
  function handleStartGame() {
    let piece_color;
    if (color === "white") {
      piece_color = true;
    } else {
      piece_color = false;
    }
    const preferences = { skill_level: stockfishlevel, color: piece_color };
    if (FEN === "start" && props.socket.connected) {
      props.socket.emit("start-game", preferences);
      setOpen(false);
    } else {
      alert("Pieces are not in starting position!");
    }
  }
  function startGame() {
    setOpen(true);
  }

  function handleResultMessage(messageDisctionary: any) {
    if (messageDisctionary.result) {
      setResult(messageDisctionary.result);
      setOpen(true);
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
  const handlePregame = (level: number, selectedSide: string) => {
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
    <div className="main-container">
      <div className="pre-game">
        <PreGame
          open={preGame}
          stockfishLevel={stockfishlevel}
          handleOK={handlePregame}
        />
      </div>
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
          handleOK={handleStartGame}
          open={open}
        />
      )}
      <div className="buttons">
        {FEN !== "start" ? (
          <>
            <Button variant="outlined" onClick={() => newGame()}>
              New game
            </Button>
            <Button variant="outlined" onClick={() => getValidMoves()}>
              Get move
            </Button>
          </>
        ) : (
          <Button variant="contained" onClick={() => startGame()}>
            Start game
          </Button>
        )}
      </div>
      <div>{valid_moves && valid_moves.map((move) => <p>{move}</p>)}</div>
    </div>
  );
}
