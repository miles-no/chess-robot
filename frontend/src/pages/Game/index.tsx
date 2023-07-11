import { Button } from "@mui/material";
import { useEffect, useState } from "react";
import { Socket } from "socket.io-client";
import AlertComponent from "../../Components/Alert/Notification";
import MyChessboard from "../../Components/Chessboard/Chessboard";
import "./index.css";
interface gameProps {
  socket: Socket;
}

export default function Game(props: gameProps) {
  const [open, setOpen] = useState<boolean>(false);
  const [result, setResult] = useState<string>();
  const [winner, setWinner] = useState<string>();
  function newGame() {
    //set FEN to "start"
    props.socket.emit("new-game", "new-game");
  }

  function startGame() {
    props.socket.emit("start-game", "startGame");
  }

  useEffect(() => {
    if (winner) {
      setWinner("White");
    } else if (winner === null) {
      setWinner("Draw");
    } else {
      setWinner("Black");
    }
  }, [winner]);

  useEffect(() => {
    if (result) {
      setResult(result);
      setOpen(true);
    }
  }, [result]);

  const handleClose = () => {
    // On closing the alert
    setOpen(false);
  };
  const handleOK = () => {
    setOpen(false);
    setResult(undefined);
    newGame();
  };

  return (
    <div className="main-container">
      <div className="alert">
        {result && (
          <AlertComponent
            open={open}
            alertTitle={result}
            message={"Winner is... " + winner}
            handleClose={handleClose}
            handleOK={handleOK}
          />
        )}
      </div>
      <div className="unclickable-area">
        <MyChessboard boardWidth={600} socket={props.socket} />
      </div>
      <div className="buttons">
        <Button onClick={() => startGame()}>Start game</Button>
        <Button onClick={() => newGame()}>New game</Button>
      </div>
    </div>
  );
}
