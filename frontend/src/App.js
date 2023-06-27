import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Header from "./Components/Header/Header";
import Data from "./pages/Data";
import Home from "./pages/Home";
function App() {
  return (
    <div className="App">
      <BrowserRouter>
      <Header/>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/data" element={<Data />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
