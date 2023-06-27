import Button from "@mui/material/Button";
import { useNavigate } from "react-router-dom";
export default function Home() {
  const navigate = useNavigate();
  function startGame() {
    navigate("/game");
  }
  return (
    <div>
      <h1>Welcome!</h1>
      <Button variant="outlined" onClick={startGame}>
        Start Game
      </Button>
    </div>
  );
}
