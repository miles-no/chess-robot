import { Box, Button } from "@mui/material";
import { useEffect, useState } from "react";
import { Socket } from "socket.io-client";
import AlertComponent from "../../Components/Alert/Notification";
import MyChessboard from "../../Components/Chessboard/Chessboard";
import GameStatus from "../../Components/GameStatus/GameStatus";
import { default as PreGame } from "../../Components/PreGame/PreGame";
import { useGameContext, GameState } from "./GameContext";
import "./index.css";
interface gameProps {
  socket: Socket;
}

export default function Game(props: gameProps) {
  const [FEN, setFEN] = useState<string>("start");
  const [moves, setMoves] = useState<string[]>();
  const [open, setOpen] = useState<boolean>(false);
  const [result, setResult] = useState<string>();
  const [winner, setWinner] = useState<string>();
  const [color, setColor] = useState<boolean>();
  const [preGame, setpreGame] = useState<boolean>(true);
  const [stockfishlevel, setStockfishLevel] = useState<number>(0);
  const [valid_moves, setValidMoves] = useState<string[]>();
  const [currentPlayer, setCurrentPlayer] = useState<boolean>(true);
  const { gameState, setGameState } = useGameContext();
  const [score, setScore] = useState<number>(0);
  const [promotion, setPromotion] = useState<string>("");
  const [player, setPlayer] = useState<string>();
  const [not_valid, setNotValid] = useState<boolean>(false);

  useEffect(() => {
    props.socket.on("invalid-move", handleInvalidMove);
    props.socket.on("valid-moves", handleValidMoves);
    props.socket.on("get-fen", handleFEN);
    props.socket.on("game-over", handleResultMessage);
    props.socket.on("promotion", handlePromotion);
    return () => {
      // Cleanup the props.socket listener when the component unmounts
      props.socket.off("invalid-move", handleInvalidMove);
      props.socket.off("valid-moves", handleValidMoves);
      props.socket.off("get-fen", handleFEN);
      props.socket.off("game-over", handleResultMessage);
    };
  }, [props.socket]);

  const newGame = async () => {
    if (gameState) {
      const confirmNewGame = window.confirm(
        "Are you sure you want to start a new game?"
      );
      if (!confirmNewGame) {
        return; // Exit early if the user cancels the new game confirmation
      }
      props.socket.emit("stop-game");
      window.confirm("Please adjust the pieces to starting positions!");
      setpreGame(true);
      setFEN("start");
    }
  };
  const handleFEN = (message: any) => {
    if (message.fen) {
      setFEN(message.fen);
      setValidMoves([]);
      setCurrentPlayer(message.color);
      setMoves(message.moves);
      setNotValid(false);
    }
  };

  const handlePromotion = (promotion: string) => {
    if (promotion) {
      setPromotion(promotion);
      setOpen(true);
    }
  };

    function startGame() {
    if (props.socket.connected) {
      const preferences = {
        skill_level: stockfishlevel,
        color: color,
        name: player,
      };
      props.socket.emit("start-game", preferences);
      setGameState(GameState.inProgress);
    } else {
      setOpen(true);
    }
  }

  function handleResultMessage(messageDictionary: any) {
    if (messageDictionary.result) {
      setResult(messageDictionary.result);
      setOpen(true);
      setGameState(GameState.hasEnded);
    }
    if (messageDictionary.winner) {
      setWinner(messageDictionary.winner);
    }
    if (messageDictionary.score) {
      setScore(messageDictionary.score);
    }
  }

  const handleInvalidMove = () => {
      setNotValid(true);
  };

  const handleOK = () => {
    setResult(undefined);
    setOpen(false);
  };

  const handlePregame = (
    level: number,
    selectedSide: boolean,
    name: string
  ) => {
    setStockfishLevel(level);
    setColor(selectedSide);
    setPlayer(name);
    setpreGame(false);
    if (gameState) {
      const preferences = {
        skill_level: level,
        color: selectedSide,
        name: player,
      };
      props.socket.emit("new-game", preferences);
    }
    if (gameState === GameState.hasEnded) {
      setGameState(GameState.inProgress);
    }
  };

  const getValidMoves = () => {
    props.socket.emit("get-valid-moves");
  };

  const getButton = () => {
    switch (gameState) {
      case GameState.hasEnded:
        return (
          <div className="game-button">
            <Button
              variant="outlined"
              onClick={() => newGame()}
              className="new-button"
            >
              New game
            </Button>
          </div>
        );
      case GameState.inProgress:
        return (
          <div className="game-button">
            <Button
              variant="outlined"
              onClick={() => newGame()}
              className="new-button"
            >
              New game
            </Button>
            <Button
              variant="outlined"
              onClick={() => getValidMoves()}
              className="moves-button"
            >
              Get move
            </Button>
          </div>
        );
      case GameState.notStarted:
        return (
          <div className="start-button">
            <Button
              variant="contained"
              onClick={() => startGame()}
              sx={{ backgroundColor: "black" }}
            >
              Start game
            </Button>
          </div>
        );
    }
  };

  const handleValidMoves = (validMoves: string[]) => { 
      setValidMoves(validMoves);
  };

  return (
    <Box>
      {preGame ? (
        <Box className="pre-game">
          <PreGame
            open={preGame}
            stockfishLevel={stockfishlevel}
            handleOK={handlePregame}
          />
        </Box>
      ) : (
        <Box className="main-container">
          <Box className="game">
            {promotion && (
              <AlertComponent
                open={open}
                alertTitle="Promotion!"
                message={
                  "Please place promoted piece: " +
                  promotion +
                  " in the correct position"
                }
                handleOK={handleOK}
              />
            )}
            <Box className="alert">
              {result && (
                <AlertComponent
                  open={open}
                  alertTitle={result}
                  message={"Winner is " + winner + ". Your score is " + score}
                  handleOK={handleOK}
                />
              )}
            </Box>
            <Box className="chessboard-box">
              <Box className="unclickable-area">
                <MyChessboard socket={props.socket} FEN={FEN} />
              </Box>
            </Box>
            {result === undefined && !gameState && (
              <AlertComponent
                alertTitle="Start Game"
                message="Make sure pieces are in starting position"
                handleOK={handleOK}
                open={open}
              />
            )}
            <Box className="buttons">{getButton()}</Box>
          </Box>
          <Box className="game-status">
            {[GameState.inProgress, GameState.hasEnded].includes(gameState) && (
              <GameStatus title="GAME" moves={moves} player={currentPlayer} />
            )}
          </Box>
          {valid_moves && valid_moves.length > 0 && (
            <Box className="valid-moves">
              <GameStatus
                title="Available moves"
                moves={valid_moves}
                player={undefined}
              />
            </Box>
                      )}
                      {(not_valid ) ? (
                          <Box className="not-valid-move">
                              <GameStatus
                                  title="Invalid move!"
                                  moves={valid_moves}
                                  player={undefined}
                              />
                          </Box> 
                      ) : <>  </>
                      }
        </Box>
      )}
    </Box>
  );
}
