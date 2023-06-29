import React, { createContext, useEffect, useState } from "react";
import { io } from "socket.io-client";

const WebSocketContext = createContext();

const WebSocketProvider = ({ children }) => {
  const [websocket, setWebsocket] = useState(io("ws://127.0.0.1:5000"));

  useEffect(() => {
    if (!websocket) {
      const newWebsocket = io("ws://127.0.0.1:5000");
      setWebsocket(newWebsocket);
    }
    return () => {
      websocket.close();
    };
  }, []);

  return (
    <WebSocketContext.Provider value={websocket}>
      {children}
    </WebSocketContext.Provider>
  );
};

export { WebSocketContext, WebSocketProvider };
