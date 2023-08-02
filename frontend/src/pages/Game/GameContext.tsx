import React, { ReactNode, createContext, useContext, useState } from "react";

interface GameContextType {
  gameInProgress: boolean;
  setGameInProgress: React.Dispatch<React.SetStateAction<boolean>>;
}

const GameContext = createContext<GameContextType | undefined>(undefined);

interface GameProviderProps {
  children: ReactNode;
}

export const GameProvider: React.FC<GameProviderProps> = ({ children }) => {
  const [gameInProgress, setGameInProgress] = useState<boolean>(false);

  const contextValue: GameContextType = {
    gameInProgress,
    setGameInProgress,
  };

  return (
    <GameContext.Provider value={contextValue}>{children}</GameContext.Provider>
  );
};

export const useGameContext = (): GameContextType => {
  const context = useContext(GameContext);
  if (!context) {
    throw new Error("useGameContext must be used within a GameProvider");
  }
  return context;
};
