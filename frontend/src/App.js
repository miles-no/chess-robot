import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Data from "./pages/Data";
import Home from "./pages/Home";
import Game from "./pages/Game";
function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/data" element={<Data />} />
          <Route path="/game" element={<Game />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
