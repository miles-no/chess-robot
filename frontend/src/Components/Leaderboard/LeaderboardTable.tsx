import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import "./LeaderboardTable.css";

interface LeaderboardTableProps {
  data?: { name: string; score: number; date: string; level: number }[];
}

export default function LeaderboardTable(props: LeaderboardTableProps) {
  return (
    <div className="leaderboardTable">
      {props.data && (
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Date</TableCell>
                <TableCell>Player</TableCell>
                <TableCell>Level</TableCell>
                <TableCell>Score</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {props.data.map((value, key) => {
                return (
                  <TableRow key={key}>
                    <TableCell>{value.date}</TableCell>
                    <TableCell component="th" scope="row">
                      {value.name}
                    </TableCell>
                    <TableCell>{value.level}</TableCell>
                    <TableCell>{value.score}</TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </TableContainer>
      )}
    </div>
  );
}
