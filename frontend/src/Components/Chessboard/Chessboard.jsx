import Button from "@mui/material/Button";
import React, { useEffect, useState } from "react";
import "./Chessboard.css";
import Tile from "./Tile";

export default function Chessboard({ size = 8, initialPieces = [], socket }) {
  const [moves, setMoves] = useState({});
  const [pieces, setPieces] = useState(initialPieces);
  const [deletedPieces, setDeletedPieces] = useState([]);
  const [result, setResult] = useState();

  const handleServerMessage = (msg) => {
    setMoves({
      prevX: msg.prevX,
      prevY: msg.prevY,
      currX: msg.nextX,
      currY: msg.nextY,
    });
  };

  // Event listener for 'from-server' event
  const handleResultMessage = (messageDictionary) => {
    if (messageDictionary.result) {
      setResult(messageDictionary.result);
    }
  };

  useEffect(() => {
    socket.on("from-server", handleServerMessage);
    // Cleanup the socket listener when the component unmounts
    return () => {
      socket.off("from-server", handleServerMessage);
    };
  }, [socket]);

  useEffect(() => {
    socket.on("from-server", handleResultMessage);

    // Clean up the event listener on component unmount
    return () => {
      socket.off("from-server", handleResultMessage);
    };
  }, []);

  useEffect(() => {
    if (moves.prevX !== undefined && moves.currX !== undefined) {
      const pieceIndex = pieces.findIndex(
        (piece) => piece.x === moves.prevX && piece.y === moves.prevY
      );

      if (pieceIndex !== -1) {
        movePiece(pieceIndex, moves.currX, moves.currY);
        checkPositions();
      }
    }
  }, [moves]);

  useEffect(() => {
    if (result) {
      alert("Game concluded: " + result + " Starting new game...");
      newGame();
    }
  }, [result]);

  const movePiece = (pieceIndex, newX, newY) => {
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
  const checkPositions = () => {
    for (let i = 0; i < pieces.length; i++) {
      if (moves.currX === pieces[i].x && moves.currY === pieces[i].y) {
        deletePiece(i);
      }
    }
  };

  const deletePiece = (index) => {
    setPieces((prevPieces) => prevPieces.filter((_, i) => i !== index));
    setDeletedPieces((prevDeletedPieces) => [
      ...prevDeletedPieces,
      pieces[index],
    ]);
  };

  const generateBoard = () => {
    let board = [];

    for (let i = size - 1; i >= 0; i--) {
      for (let j = 0; j < size; j++) {
        const number = i + j + 2;
        let image = undefined;

        pieces.forEach((piece, index) => {
          if (piece.x === j && piece.y === i) {
            image = piece.image;
          }
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
            onPieceMove={(index, newX, newY) => movePiece(index, newX, newY)}
          />
        );
      }
    }

    return board;
  };

  const sendToServer = () => {
    socket.emit("to-server", "hello");
  };

  function newGame() {
    if (pieces !== initialPieces || deletedPieces.length !== 0) {
      const confirmNewGame = window.confirm(
        "Are you sure you want to start a new game?"
      );
      if (!confirmNewGame) {
        return; // Exit early if the user cancels the new game confirmation
      }
    }

    setPieces(initialPieces);
    setDeletedPieces([]);
    socket.emit("new-game", "Start new game");
  }

  function startGame() {
    socket.emit("start-game", "Start game");
  }

  return (
    <div className="main-box">
      <h1>Chessboard</h1>
      <div className="Chessboardcontainer">
        <div id="chessboard">{generateBoard()}</div>
        <div className="coordinates">
          {Array.from({ length: size }, (_, index) => (
            <h1 key={index}>{String(size - index)}</h1>
          ))}
        </div>
        <Button
          sx={{
            placeSelf: "center end",
          }}
          onClick={sendToServer}
        >
          Move
        </Button>
        <div className="GraveyardContainer" style={{ paddingTop: "3em" }}>
          <h1>Graveyard</h1>
          <div className="Graveyard">
            {deletedPieces.map((dPiece, index) => (
              <img
                className="graveyardpieces"
                key={index}
                src={dPiece.image}
                alt={`Piece ${index}`}
                style={{ width: "70px", height: "70px" }}
              />
            ))}
          </div>
          <div>
            <Button onClick={newGame}>New Game</Button>
          </div>
          <div>
            <Button onClick={startGame}>Start Game</Button>
          </div>
        </div>
      </div>
    </div>
  );
}
