import React, { createContext, useEffect, useState } from "react";

const WebSocketContext = createContext();

const WebSocketProvider = ({ children }) => {
  const [websocket, setWebsocket] = useState(null);

  useEffect(() => {
    const newWebsocket = new WebSocket("ws://localhost:8000");
    setWebsocket(newWebsocket);

    return () => {
      newWebsocket.close();
    };
  }, []);

  return (
    <WebSocketContext.Provider value={websocket}>
      {children}
    </WebSocketContext.Provider>
  );
};

export { WebSocketContext, WebSocketProvider };
