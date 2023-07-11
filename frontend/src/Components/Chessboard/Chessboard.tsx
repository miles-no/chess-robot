import { Chessboard } from "react-chessboard";
import { Socket } from "socket.io-client";
interface mychessboardProps {
  boardWidth: number;
  FEN: string;
  socket: Socket;
}
export default function MyChessboard(props: mychessboardProps) {
  return <Chessboard boardWidth={props.boardWidth} position={props.FEN} />;
}
