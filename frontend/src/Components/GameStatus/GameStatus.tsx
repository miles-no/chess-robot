import { Box, Typography } from "@mui/material";
import { useEffect, useState } from "react";

interface gameStatusProps {
  player: boolean | undefined;
  moves: string[] | undefined;
}
export default function GameStatus(props: gameStatusProps) {
  return (
    <Box
      sx={{
        padding: "0.02em",
        width: "30em",
      }}
    >
      <Box
        sx={{
          borderRadius: "8px",
          backgroundColor: "#F2F2F2",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          color: "black",
          fontSize: "24px",
          fontWeight: "bold",
          boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)",
        }}
      >
        <Typography variant="h4" gutterBottom>
          GAME
        </Typography>
        {props.player ? (
          <Typography variant="h5">Turn: White</Typography>
        ) : (
          <Typography variant="h5">Turn: Black</Typography>
        )}
        {props.moves &&
          props.moves.map((move) => (
            <Typography variant="h6">{move}</Typography>
          ))}
      </Box>
    </Box>
  );
}
