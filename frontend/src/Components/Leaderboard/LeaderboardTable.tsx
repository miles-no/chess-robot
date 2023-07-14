import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import "./LeaderboardTable.css";

export default function LeaderboardTable() {
  const data = [
    { name: "Player 1", score: 100 },
    { name: "Player 2", score: 200 },
    { name: "Player 3", score: 300 },
  ];

  return (
    <div className="leaderboardTable">
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Player</TableCell>
              <TableCell>Score</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((value, key) => {
              return (
                <TableRow key={key}>
                  <TableCell component="th" scope="row">
                    {value.name}
                  </TableCell>
                  <TableCell>{value.score}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </div>
  );
}
