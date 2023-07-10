import { PieceType } from "../types/pieceType";
export function getPieces(): Array<PieceType> {
  var pieces: PieceType[] = [];
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
  return pieces;
}
