import { useEffect, useState } from "react";
import { Chessboard } from "react-chessboard";
import { Socket } from "socket.io-client";
interface mychessboardProps {
  socket: Socket;
}
export default function MyChessboard(props: mychessboardProps) {
  const [FEN, setFEN] = useState<string>(
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
  );

  useEffect(() => {
    props.socket.on("get-fen", handleFEN);
    // Cleanup the props.socket listener when the component unmounts
    return () => {
      props.socket.off("get-fen", handleFEN);
    };
  }, [props.socket]);

  const handleFEN = (fen: string) => {
    console.log(fen);
    if (fen) {
      setFEN(fen);
      console.log(fen);
    }
  };

  return (
    <div>
      <Chessboard boardWidth={500} position={FEN} />
    </div>
  );
}
