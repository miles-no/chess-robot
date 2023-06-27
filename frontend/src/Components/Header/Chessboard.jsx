import "./Chessboard.css";
import Tile from "./Tile";
export default function Chessboard() {
  const verticalAxis = ["1", "2", "3", "4", "5", "6", "7", "8"];
  const horizontalAxis = ["a", "b", "c", "d", "e", "f", "g", "h"];

  const pieces = [];

  for (let i = 0; i < 8; i++) {
    pieces.push({ image: "assets/images/black-pawn.png", x: i, y: 6 });
  }

  for (let i = 0; i < 8; i++) {
    pieces.push({ image: "assets/images/white-pawn.png", x: i, y: 1 });
  }

  let board = [];

  for (let i = verticalAxis.length - 1; i >= 0; i--) {
    for (let j = 0; j < horizontalAxis.length; j++) {
      const number = i + j + 2;
      let image = undefined;

      pieces.forEach((p) => {
        if (p.x === j && p.y === i) image = p.image;
      });

      board.push(<Tile number={number} image={image} />);
    }
  }

  return (
    <div>
      <h1>Chessboard</h1>
      <div id="chessboard">{board}</div>
    </div>
  );
}
