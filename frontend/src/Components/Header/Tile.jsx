import "./Tile.css";

export default function Tile(props) {
  console.log(props.number);
  if (props.number % 2 === 0) {
    return (
      <div className="tile white-tile">
        <img src={props.image} alt=" " />
      </div>
    );
  } else {
    return (
      <div className="tile black-tile">
        <img src={props.image} alt=" " />
      </div>
    );
  }
}
