export function handleFEN(fen: string): Array<string> {
  const fenArray = fen.split("/").slice(0, 8);
  const lastElement = fenArray[7].split(" ")[0];
  fenArray[7] = lastElement;
  console.log(fenArray);
  return fenArray;
}
