import Button from "@mui/material/Button";
import React, { useState } from "react";
import "./Chessboard.css";
import Tile from "./Tile";
export default function Chessboard({ size = 8, initialPieces = [] }) {
  const [moves, setMoves] = useState([[]]);

  function getMoves() {
    fetch("/moves")
      .then((res) => res.json())
      .then((data) => {
        setMoves({
          prevX: data.prevX,
          prevY: data.prevY,
          currX: data.nextX,
          currY: data.nextY,
        });
      });
    console.log(moves);
    moveButton();
  }
  React.useEffect(() => {}, []);

  const verticalAxis = Array.from({ length: size }, (_, index) =>
    String(index + 1)
  );
  const horizontalAxis = Array.from({ length: size }, (_, index) =>
    String.fromCharCode(97 + index)
  );

  const [pieces, setPieces] = useState(initialPieces);

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

  let board = [];

  for (let i = verticalAxis.length - 1; i >= 0; i--) {
    for (let j = 0; j < horizontalAxis.length; j++) {
      const number = i + j + 2;
      let image = undefined;

      pieces.forEach((p, index) => {
        if (p.x === j && p.y === i) image = p.image;
      });

      const coordinateX = `${horizontalAxis[j]}`;
      const coordinateY = `${verticalAxis[i]}`;

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

  function moveButton() {
    let index;
    for (let i = 0; i < pieces.length; i++) {
      if (pieces[i].x === moves.prevX && pieces[i].y === moves.prevY) {
        index = i;
      }
    }
    handlePieceMove(index, moves.currX, moves.currY);
  }

  return (
    <div>
      <h1>Chessboard</h1>
      <div className="Chessboardcontainer">
        <div id="chessboard">{board}</div>
        <div className="coordinates">
          {verticalAxis.reverse().map((coordinate, index) => (
            <h1 key={index}>{coordinate}</h1>
          ))}
        </div>
        <Button onClick={() => getMoves()}>Move</Button>
      </div>
    </div>
  );
}
