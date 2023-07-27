import { Socket } from "socket.io-client";
import LeaderboardTable from "../../Components/Leaderboard/LeaderboardTable";
import { useEffect, useState } from "react";
import { DialogTitle } from "@mui/material";

interface leaderboardProps {
  socket: Socket;
}

export default function Leaderboard(props: leaderboardProps) {
  const [leaderboard, setLeaderboard] =
    useState<{ name: string; score: number; date: string; level: number }[]>();

  useEffect(() => {
    props.socket.emit("get-leaderboard");
    props.socket.on("leaderboard", getLeaderboard);
    return () => {
      props.socket.off("get-leaderboard");
      props.socket.off("leaderboard", getLeaderboard);
    };
  }, [props.socket]);

  const getLeaderboard = (
    data: { name: string; score: number; date: string; level: number }[]
  ) => {
    setLeaderboard(data);
  };

  return (
    <div>
      <DialogTitle sx={{ textAlign: "center" }}>Leaderboard</DialogTitle>
      <LeaderboardTable data={leaderboard} />
    </div>
  );
}
