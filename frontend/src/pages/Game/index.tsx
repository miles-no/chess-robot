import { Button } from "@mui/material";
import { Socket } from "socket.io-client";
import MyChessboard from "../../Components/Chessboard/Chessboard";
import "./index.css";
interface gameProps {
  socket: Socket;
}

export default function Game(props: gameProps) {
  function newGame() {
    props.socket.emit("new-game", "new-game");
  }

  function startGame() {
    props.socket.emit("start-game", "startGame");
  }

  return (
    <div className="main-container">
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
