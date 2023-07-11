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
  const [FEN, setFEN] = useState<string>("start");
  const [open, setOpen] = useState<boolean>(false);
  const [result, setResult] = useState<string>();
  const [winner, setWinner] = useState<string>();
  function newGame() {
    //set FEN to "start"
    setFEN("start");
    props.socket.emit("new-game", "new-game");
  }
  useEffect(() => {
    props.socket.on("get-fen", handleFEN);
    // Cleanup the props.socket listener when the component unmounts
    return () => {
      props.socket.off("get-fen", handleFEN);
    };
  }, [props.socket]);

  const handleFEN = (fen: string) => {
    if (fen) {
      setFEN(fen);
    }
  };
  function startGame() {
    props.socket.emit("start-game", "startGame");
  }

  useEffect(() => {
    props.socket.on("game-over", handleResultMessage);

    // Clean up the event listener on component unmount
    return () => {
      props.socket.off("game-over", handleResultMessage);
    };
  }, [props.socket]);

  function handleResultMessage(messageDisctionary: any) {
    if (messageDisctionary.result) {
      setResult(messageDisctionary.result);
      setOpen(true);
    }
    if (messageDisctionary.winner) {
      setWinner(messageDisctionary.winner);
    }
  }

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
            message={"Winner is " + winner}
            handleClose={handleClose}
            handleOK={handleOK}
          />
        )}
      </div>
      <div className="unclickable-area">
        <MyChessboard boardWidth={600} socket={props.socket} FEN={FEN} />
      </div>
      <div className="buttons">
        <Button onClick={() => startGame()}>Start game</Button>
        <Button onClick={() => newGame()}>New game</Button>
      </div>
    </div>
  );
}
