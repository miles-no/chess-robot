import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Header from "./Components/Header/Header";
import Data from "./pages/Data";
import Game from "./pages/Game";
import Home from "./pages/Home";
function App() {
  return (
    <div className="App">
      <BrowserRouter>
      <Header/>
      <div style={{paddingTop: "4em"}}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/data" element={<Data />} />
          <Route path="/game" element={<Game />} />
        </Routes>
        </div>
      </BrowserRouter>
    </div>
  );
}

export default App;
