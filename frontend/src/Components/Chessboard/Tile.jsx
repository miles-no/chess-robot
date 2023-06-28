import "./Tile.css";

export default function Tile(props) {
  if (props.number % 2 === 0) {
    return (
      <div>
        <div className="tile white-tile">
          {props.image && (
            <div
              className="chess-piece"
              style={{ backgroundImage: `url(${props.image})` }}
            ></div>
          )}
        </div>
        <div className="tile coordinate">
          <h1>{props.coordinatesX}</h1>
        </div>
      </div>
    );
  } else {
    return (
      <div>
        <div className="tile black-tile">
          {props.image && (
            <div
              className="chess-piece"
              style={{ backgroundImage: `url(${props.image})` }}
            ></div>
          )}
        </div>
        <div className="tile coordinate">
          <h1>{props.coordinatesX}</h1>
        </div>
      </div>
    );
  }
}
