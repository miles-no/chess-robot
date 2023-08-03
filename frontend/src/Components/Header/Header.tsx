import { Avatar, Button } from "@mui/material";
import Box from "@mui/material/Box";
import { useNavigate } from "react-router-dom";
import { Socket } from "socket.io-client";
import { GameState, useGameContext } from "../../pages/Game/GameContext";
import { useState } from "react";

interface headerProps {
  socket: Socket;
}

export default function Header(props: headerProps) {
  const navigate = useNavigate();
  const { gameState, setGameState } = useGameContext();
  const [disabled, setDisabled] = useState(false);
  const handleHome = () => {
    if (gameState === GameState.inProgress) {
      setDisabled(true);
    } else {
      navigate("");
    }
  };

  return (
    <Box
      id="main-container"
      sx={{
        position: "absolute",
        backgroundColor: "white",
        width: "100%",
        height: "4em",

        display: "flex",
        justifyContent: "stretch",
        borderBottom: "1px solid black",
        zIndex: 10,
      }}
    >
      <Box
        sx={{
          display: "flex",
          justifyContent: "left",
          width: "80%",
          height: "90%",
          paddingLeft: "2%",
        }}
      >
        <Button
          onClick={handleHome}
          sx={{
            width: "10em",
            height: "auto",
          }}
          disabled={disabled}
          startIcon={
            <Avatar
              src="https://www.miles.no/wp-content/uploads/2020/11/miles_logo_red_rgb.jpg"
              alt="Miles logo"
              variant="square"
              sx={{
                width: "100%",
                height: "100%",
              }}
            />
          }
        ></Button>
      </Box>
      <Box
        sx={{
          display: "flex",
          justifyContent: "right",
          width: "80%",
          paddingRight: "2%",
        }}
      >
        <Button
          onClick={() => navigate("")}
          sx={{
            width: "3em",
            height: "100%",
            borderRadius: "50%",
          }}
        >
          <Avatar sx={{ width: "80%", bgcolor: "black" }} />
        </Button>
      </Box>
    </Box>
  );
}
