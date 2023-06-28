import "./Chessboard.css";
import Tile from "./Tile";
export default function Chessboard() {
  const verticalAxis = ["1", "2", "3", "4", "5", "6", "7", "8"];
  const horizontalAxis = ["a", "b", "c", "d", "e", "f", "g", "h"];

  const pieces = [];
  const coordinates = [];
  for (let p = 0; p < 2; p++) {
    const type = p === 0 ? "b" : "w";
    const y = p === 0 ? 7 : 0;

    pieces.push({ image: `assets/images/rook_${type}.png`, x: 0, y });
    pieces.push({ image: `assets/images/rook_${type}.png`, x: 7, y });
    pieces.push({ image: `assets/images/knight_${type}.png`, x: 1, y });
    pieces.push({ image: `assets/images/knight_${type}.png`, x: 6, y });
    pieces.push({ image: `assets/images/bishop_${type}.png`, x: 2, y });
    pieces.push({ image: `assets/images/bishop_${type}.png`, x: 5, y });
    pieces.push({ image: `assets/images/queen_${type}.png`, x: 3, y });
    pieces.push({ image: `assets/images/king_${type}.png`, x: 4, y });
  }

  for (let i = 0; i < 8; i++) {
    pieces.push({ image: "assets/images/pawn_b.png", x: i, y: 6 });
  }

  for (let i = 0; i < 8; i++) {
    pieces.push({ image: "assets/images/pawn_w.png", x: i, y: 1 });
  }

  let board = [];

  for (let i = verticalAxis.length - 1; i >= 0; i--) {
    coordinates.push({ x: horizontalAxis[i], y: i + 1 });
    for (let j = 0; j < horizontalAxis.length; j++) {
      const number = i + j + 2;
      let image = undefined;

      pieces.forEach((p) => {
        if (p.x === j && p.y === i) image = p.image;
      });
      const coordinateX = `${horizontalAxis[j]}`;
      board.push(
        <Tile
          key={`${i},${j}`}
          number={number}
          image={image}
          coordinatesX={coordinateX}
        />
      );
    }
  }

  return (
    <div>
      <h1>Chessboard</h1>
    <div className="Chessboardcontainer">
      <div id="chessboard">{board}</div>
      <div className="coordinates">
          {verticalAxis.map((coordinate, index) => (
            <h1 key={index}>{coordinate}</h1>
          ))}
        </div>
    </div>
    </div>
  );
}
