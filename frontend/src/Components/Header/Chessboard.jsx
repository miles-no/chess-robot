import "./Chessboard.css";
export default function Chessboard() {
  const verticalAxis = ["1", "2", "3", "4", "5", "6", "7", "8"];
  const horizontalAxis = ["a", "b", "c", "d", "e", "f", "g", "h"];
  let board = [];

  for (let i = verticalAxis.length - 1; i >= 0; i--) {
    for (let j = 0; j < horizontalAxis.length; j++) {
      const number = i + j + 2;

      if (number % 2 === 0) {
        board.push(<div className="white-tile"></div>);
      } else {
        board.push(<div className="black-tile"></div>);
      }
    }
  }

  return (
    <div>
      <h1>Chessboard</h1>
      <div id="chessboard">{board}</div>
    </div>
  );
}
