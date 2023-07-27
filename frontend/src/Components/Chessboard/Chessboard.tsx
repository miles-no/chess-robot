import { Chessboard } from "react-chessboard";
import { Socket } from "socket.io-client";
interface mychessboardProps {
  FEN: string;
  socket: Socket;
}
export default function MyChessboard(props: mychessboardProps) {
  return <Chessboard position={props.FEN} />;
}
