import Button from "@mui/material/Button";
import React, { useEffect, useState } from "react";
import { PieceType } from "../../Components/Chessboard/types/pieceType";
import "./Chessboard.css";
import Tile from "./Tile";
import { chessPieceNotation } from "./chessDictionary";
import { Moves } from "./types/moves";
import { Promo } from "./types/promo";
interface chessboardProps {
  size: number;
  initialPieces: PieceType[];
  socket: any;
}
export default function Chessboard(props: chessboardProps) {
  const [moves, setMoves] = useState<Moves>();
  const [pieces, setPieces] = useState<PieceType[]>(props.initialPieces);
  const [deletedPieces, setDeletedPieces] = useState<PieceType[]>([]);
  const [result, setResult] = useState();

  const deletedPiecesRef = React.useRef(deletedPieces);
  const piecesRef = React.useRef(pieces);
  useEffect(() => {
    piecesRef.current = pieces;
  }, [pieces]);
  useEffect(() => {
    deletedPiecesRef.current = deletedPieces;
  }, [deletedPieces]);
  const handleServerMessage = (msg: any) => {
    setMoves({
      prevX: msg.prevX,
      prevY: msg.prevY,
      currX: msg.nextX,
      currY: msg.nextY,
    });
  };

  // Event listener for 'from-server' event
  const handleResultMessage = (messageDictionary: any) => {
    if (messageDictionary.result) {
      setResult(messageDictionary.result);
    }
  };

  const validationError = () => {
    alert("Invalid move, try again.");
  };

  const handlePassant = (passant: any) => {
    const piecesList = piecesRef.current;
    const pawnToBeRemoved = piecesList.findIndex(
      (piece) => piece.x === passant.currX && piece.y === passant.currY
    );
    deletePiece(pawnToBeRemoved);
  };

  useEffect(() => {
    props.socket.on("from-server", handleServerMessage);
    // Cleanup the props.socket listener when the component unmounts
    return () => {
      props.socket.off("from-server", handleServerMessage);
    };
  }, [props.socket]);

  useEffect(() => {
    props.socket.on("from-server", handleResultMessage);

    // Clean up the event listener on component unmount
    return () => {
      props.socket.off("from-server", handleResultMessage);
    };
  }, []);

  useEffect(() => {
    // Set up the event listeners
    props.socket.on("promotion", handlePromotion);
    props.socket.on("validation-error", validationError);
    props.socket.on("passant", handlePassant);

    // Clean up the event listeners on component unmount
    return () => {
      props.socket.off("promotion", handlePromotion);
      props.socket.off("validation-error", validationError);
      props.socket.off("passant", handlePassant);
    };
  }, []);

  useEffect(() => {
    if (moves) {
      if (moves.prevX !== undefined && moves.currX !== undefined) {
        const pieceIndex = pieces.findIndex(
          (piece) => piece.x === moves.prevX && piece.y === moves.prevY
        );

        if (pieceIndex !== -1 && moves.currY) {
          movePiece(pieceIndex, moves.currX, moves.currY);
          checkPositions();
        }
      }
    }
  }, [moves]);

  useEffect(() => {
    if (result) {
      alert("Game concluded: " + result + " Starting new game...");
      newGame();
    }
  }, [result]);

  const movePiece = (pieceIndex: number, newX: number, newY: number) => {
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
      if (moves) {
        if (moves.currX === pieces[i].x && moves.currY === pieces[i].y) {
          deletePiece(i);
        }
      }
    }
  };

  const deletePiece = (index: number) => {
    setPieces((prevPieces) => prevPieces.filter((_, i) => i !== index));
    setDeletedPieces((prevDeletedPieces: PieceType[]) => [
      ...prevDeletedPieces,
      pieces[index],
    ]);
  };

  const handlePromotion = (promo: Promo) => {
    const piecesList = piecesRef.current;
    const pawnToBeReplaced = piecesList.findIndex(
      (piece) => piece.x === promo.currX && piece.y === promo.currY
    );
    const imageReplacement = piecesList[pawnToBeReplaced].image;
    const deletedPiecesList = deletedPiecesRef.current;
    const pieceToBeReplaced = deletedPiecesList.findIndex((piece) =>
      piece.image.includes(
        chessPieceNotation[promo.promotion as keyof typeof chessPieceNotation] +
          "_" +
          promo.turn.charAt(0)
      )
    );
    const pieceReplaceImage = deletedPiecesList[pieceToBeReplaced].image;
    setPieces((prevPiece) => {
      const updatedPieces = [...prevPiece];
      updatedPieces[pawnToBeReplaced] = {
        image: pieceReplaceImage,
        x: promo.currX,
        y: promo.currY,
      };
      return updatedPieces;
    });
    setDeletedPieces((prevPiece) => {
      const updatedPieces = [...prevPiece];
      updatedPieces[pieceToBeReplaced] = {
        image: imageReplacement,
        x: promo.currX,
        y: promo.currY,
      };
      return updatedPieces;
    });
  };

  const generateBoard = () => {
    let board = [];

    for (let i = props.size - 1; i >= 0; i--) {
      for (let j = 0; j < props.size; j++) {
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
            onPieceMove={(index: number, newX: number, newY: number) =>
              movePiece(index, newX, newY)
            }
          />
        );
      }
    }

    return board;
  };

  function newGame() {
    if (pieces !== props.initialPieces || deletedPieces.length !== 0) {
      const confirmNewGame = window.confirm(
        "Are you sure you want to start a new game?"
      );
      if (!confirmNewGame) {
        return; // Exit early if the user cancels the new game confirmation
      }
      setResult(undefined);
    }

    setPieces(props.initialPieces);
    setDeletedPieces([]);
    props.socket.emit("new-game", "Start new game");
  }

  function startGame() {
    props.socket.emit("start-game", "Start game");
  }

  return (
    <div className="main-box">
      <h1>Chessboard</h1>
      <div className="Chessboardcontainer">
        <div id="chessboard">{generateBoard()}</div>
        <div className="coordinates">
          {Array.from({ length: props.size }, (_, index) => (
            <h1 key={index}>{String(props.size - index)}</h1>
          ))}
        </div>
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
