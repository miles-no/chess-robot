import { Chessboard } from "react-chessboard";
import { Socket } from "socket.io-client";

interface mychessboardProps {
  FEN: string;
  socket: Socket;
  rotation?: "white" | "black";
  lastMove?: string;
}

export default function MyChessboard(props: mychessboardProps) {
  // Get the from/to squares from lastMove (e.g., "e2e4" => "e2", "e4")
  const from = props.lastMove?.slice(0, 2);
  const to = props.lastMove?.slice(2, 4);

  // Build custom styles for those squares
  const customSquareStyles: Record<string, React.CSSProperties> = {};
if (from) customSquareStyles[from] = { background: "rgba(255, 255, 0, 0.4)" };
if (to) customSquareStyles[to] = { background: "rgba(255, 255, 0, 0.4)" };

  return (
    <Chessboard
      position={props.FEN}
      boardOrientation={props.rotation ?? "white"}
      customSquareStyles={customSquareStyles}
    />
  );
}