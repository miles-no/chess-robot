import Button from "@mui/material/Button";
import React, { useEffect, useState } from "react";
import "./Chessboard.css";
import Tile from "./Tile";

export default function Chessboard({ size = 8, initialPieces = [], socket }) {
  const [moves, setMoves] = useState({});
  const [pieces, setPieces] = useState(initialPieces);

  useEffect(() => {
    socket.on("from-server", (msg) => {
      setMoves({
        prevX: msg.prevX,
        prevY: msg.prevY,
        currX: msg.nextX,
        currY: msg.nextY,
      });
    });

    // Cleanup the socket listener when the component unmounts
    return () => {
      socket.off("from-server");
    };
  }, [socket]);

  useEffect(() => {
    if (moves.prevX !== undefined && moves.currX !== undefined) {
      const pieceIndex = pieces.findIndex(
        (piece) => piece.x === moves.prevX && piece.y === moves.prevY
      );

      if (pieceIndex !== -1) {
        handlePieceMove(pieceIndex, moves.currX, moves.currY);
        check_positions();
      }
    }
  }, [moves]);

  const handlePieceMove = (pieceIndex, newX, newY) => {
    setPieces((prevPieces) => {
      const updatedPieces = [...prevPieces];
      updatedPieces[pieceIndex] = {
        ...updatedPieces[pieceIndex],
        x: newX,
        y: newY,
      };
      return updatedPieces;
    });
  };

  function check_positions() {
    console.log(moves);
    for (let i = 0; i < pieces.length; i++) {
      if (moves.currX === pieces[i].x && moves.currY === pieces[i].y) {
        deleteItem(i);
      }
    }
  }

  const deleteItem = (index) => {
    setPieces((todos) => todos.filter((item, i) => i !== index));
  };

  let board = [];

  for (let i = size - 1; i >= 0; i--) {
    for (let j = 0; j < size; j++) {
      const number = i + j + 2;
      let image = undefined;

      pieces.forEach((p, index) => {
        if (p.x === j && p.y === i) image = p.image;
      });

      const coordinateX = String.fromCharCode(97 + j);
      const coordinateY = String(i + 1);

      board.push(
        <Tile
          key={`${i},${j}`}
          number={number}
          image={image}
          coordinatesX={coordinateX}
          coordinatesY={coordinateY}
          onPieceMove={(index, newX, newY) =>
            handlePieceMove(index, newX, newY)
          }
        />
      );
    }
  }

  const sendToServer = () => {
    socket.emit("to-server", "hello");
  };

  return (
    <div>
      <h1>Chessboard</h1>
      <div className="Chessboardcontainer">
        <div id="chessboard">{board}</div>
        <div className="coordinates">
          {Array.from({ length: size }, (_, index) => (
            <h1 key={index}>{String(size - index)}</h1>
          ))}
        </div>
        <Button onClick={sendToServer}>Move</Button>
        <p>
          Moves: {moves.prevX} {moves.prevY} to {moves.currX} {moves.currY}
        </p>
      </div>
    </div>
  );
}
