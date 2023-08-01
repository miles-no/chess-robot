import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { io } from "socket.io-client";
import Header from "./Components/Header/Header";
import Game from "./pages/Game";
import Home from "./pages/Home";
import Leaderboard from "./pages/Leaderboard";
function App() {
  const [socket] = React.useState(io("ws://127.0.0.1:5000"));
  return (
    <div className="App">
      <BrowserRouter>
        <Header socket={socket} />
        <div style={{ paddingTop: "4em" }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/game" element={<Game socket={socket} />} />
            <Route
              path="/leaderboard"
              element={<Leaderboard socket={socket} />}
            />
          </Routes>
        </div>
      </BrowserRouter>
    </div>
  );
}

export default App;
