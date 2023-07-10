import { Button } from "@mui/material";
import { Socket } from "socket.io-client";
import MyChessboard from "../../Components/Chessboard/Chessboard";

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
    <div>
      <MyChessboard socket={props.socket} />
      <Button onClick={() => startGame()}>Start game</Button>
      <Button onClick={() => newGame()}>New game</Button>
    </div>
  );
}
