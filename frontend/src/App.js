import React, { useEffect, useState } from "react";
import {
  BrowserRouter,
  Navigate,
  Route,
  BrowserRouter as Router,
  Routes,
} from "react-router-dom";
import Home from "./pages/Home";
function App() {
  return (
    <div className="App">
      <BrowserRouter>
          <Routes>
            <Route
              path="/home"
              element={
                  <Home />
              }
            />
          </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;