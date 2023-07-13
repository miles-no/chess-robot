import { Box } from "@mui/material";
import { useEffect, useState } from "react";

interface gameStatusProps {
  time: number;
  player: boolean | undefined;
}
export default function GameStatus(props: gameStatusProps) {
  return (
    <Box
      sx={{
        backgroundColor: "black",
        padding: "0.5em",
        width: "30em",
      }}
    >
      <Box sx={{ backgroundColor: "lightGrey" }}>
        <h1>Game</h1>
        <p>{props.time}</p>
        {props.player ? <p>Player: White</p> : <p>Player: Black</p>}
      </Box>
    </Box>
  );
}
