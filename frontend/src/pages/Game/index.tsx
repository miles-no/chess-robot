import React, { useContext } from "react";
import { Socket } from "socket.io-client";
import { getAutomaticTypeDirectiveNames } from "typescript";
import { getPieces } from "../../helpers/pieces";
import { PieceType } from "../../types/pieceType";

interface gameProps {
  socket: Socket;
}

export default function Game(props: gameProps) {
  const pieces = getPieces();
  return (
    <div>
      <h1>Chessboard here</h1>
    </div>
  );
}
