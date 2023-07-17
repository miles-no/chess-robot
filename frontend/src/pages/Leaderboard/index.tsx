import { Socket } from "socket.io-client";
import LeaderboardTable from "../../Components/Leaderboard/LeaderboardTable";
import { useEffect, useState } from "react";

interface leaderboardProps {
  socket: Socket;
}

export default function Leaderboard(props: leaderboardProps) {
  const [leaderboard, setLeaderboard] =
    useState<{ name: string; score: number }[]>();

  useEffect(() => {
    props.socket.emit("get-leaderboard");
    props.socket.on("leaderboard", getLeaderboard);
    return () => {
      props.socket.off("get-leaderboard");
      props.socket.off("leaderboard", getLeaderboard);
    };
  }, [props.socket]);

  const getLeaderboard = (data: { name: string; score: number }[]) => {
    setLeaderboard(data);
  };

  return (
    <div>
      <h1>Leaderboard</h1>
      <LeaderboardTable data={leaderboard} />
    </div>
  );
}
