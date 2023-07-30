import { Box, Typography } from "@mui/material";

interface gameStatusProps {
  player: boolean | undefined;
  moves: string[] | undefined;
  title: string;
}
export default function GameStatus(props: gameStatusProps) {
  return (
    <Box
      sx={{
        padding: "0.02em",
        width: "100%",
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
          padding: "1em",
        }}
      >
        <Typography variant="h4" gutterBottom>
          {props.title}
        </Typography>
        {props.player === undefined ? (
          <Typography variant="h5"></Typography>
        ) : props.player ? (
          <Typography variant="h5">Turn: White</Typography>
        ) : (
          <Typography variant="h5">Turn: Black</Typography>
        )}
        {props.moves &&
          props.moves.map((move, index) => (
            <Typography key={index} variant="h6">
              {move}
            </Typography>
          ))}
      </Box>
    </Box>
  );
}
