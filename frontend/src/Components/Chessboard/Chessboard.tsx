import { Chessboard } from "react-chessboard";
import { Socket } from "socket.io-client";

interface mychessboardProps {
  FEN: string;
  socket: Socket;
  rotation?: "white" | "black";
}

export default function MyChessboard(props: mychessboardProps) {
  return (
    <Chessboard
      //customBoardStyle={{ rotate: "180deg" }}
      position={props.FEN}
      boardOrientation={props.rotation ?? "white"}
    />
  );
}
