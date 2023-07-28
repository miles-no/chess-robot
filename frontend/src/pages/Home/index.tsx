import Button from "@mui/material/Button";
import { useNavigate } from "react-router-dom";
import "./index.css";

export default function Home() {
  const navigate = useNavigate();
  function startGame() {
    navigate("/game");
  }
  function viewLeaderboard() {
    navigate("/leaderboard");
  }
  return (
    <div className="main-container">
      <h1>Welcome!</h1>
      <div className="textfield">
        <p>Are you ready to crush Moxon in chess?</p>
        <p>
          Before you start your gaming adventure, kindly provide your name,
          select your preferred color, and set your desired skill level. Should
          you encounter any challenges along the way, hints are at your
          disposal. However, do keep in mind that each hint you get will lead to
          a deduction in your final score. Once the game concludes, you can view
          your results on the leaderboard.
        </p>
        <p>Good Luck!</p>
      </div>
      <div className="buttons">
        <Button variant="outlined" onClick={startGame} className="button">
          Start Game
        </Button>
        <Button variant="outlined" onClick={viewLeaderboard} className="button">
          View Leaderboard
        </Button>
      </div>
    </div>
  );
}
