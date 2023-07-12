import {
  Box,
  Button,
  Card,
  CardActionArea,
  CardContent,
  CardMedia,
  Dialog,
  DialogActions,
  DialogTitle,
  Grid,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";
//import blackKing from "../../../public/assets/images/king_b";
// import whiteKing from "../../../public/assets/images/king_w";
interface alertProps {
  open: boolean;
  stockfishLevel: number;
  handleOK: (level: number, selectedCard: string) => void;
}

export default function PreGame(props: alertProps) {
  const [level, setLevel] = useState(0);
  const [selectedCard, setSelectedCard] = useState<string | null>(null);

  const handleBackdropClick = (event: React.MouseEvent<HTMLDivElement>) => {
    event.stopPropagation();
  };

  return (
    <Dialog
      open={props.open}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
      onClick={handleBackdropClick}
      disableEscapeKeyDown
      PaperProps={{
        sx: {
          overflow: "hidden",
          // Add your custom styles to the Paper component
          // Add any other desired styles
        },
      }}
    >
      <DialogTitle id="alert-dialog-title">Pick your side</DialogTitle>
      <Grid
        sx={{
          padding: "3em",
          margin: "0 auto",
          display: "flex",
        }}
        container
        spacing={2}
      >
        <Grid item>
          <Card
            sx={{
              width: 200,
            }}
          >
            <CardActionArea
              onClick={() => {
                setSelectedCard("white");
              }}
            >
              <CardMedia
                sx={{ padding: "0 2em 2em 0em", objectFit: "contain" }}
                component="img"
                height="100"
                //image={whiteKing}
                alt="White piece"
              />
              <CardContent>
                <Typography
                  gutterBottom
                  variant="h5"
                  component="div"
                  sx={{
                    color: selectedCard === "white" ? "lightgreen" : "black",
                  }}
                >
                  White
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>
        <Grid item>
          <Card sx={{ width: 200, backgroundColor: "black", color: "white" }}>
            <CardActionArea
              onClick={() => {
                setSelectedCard("black");
              }}
            >
              <CardMedia
                sx={{ padding: "0 2em 2em 0em", objectFit: "contain" }}
                component="img"
                height="100"
                //image={blackKing}
                alt="black piece"
              />
              <CardContent>
                <Typography
                  gutterBottom
                  variant="h5"
                  component="div"
                  sx={{
                    color: selectedCard === "black" ? "lightgreen" : "white",
                  }}
                >
                  Black
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>
        <Box sx={{ paddingTop: "1em" }}>
          <Typography>Set stockfish level(1-20)</Typography>
          <TextField
            value={level}
            type="number"
            inputProps={{ min: 1, max: 20 }}
            onChange={(e) => setLevel(Number(e.target.value))}
          />
        </Box>
      </Grid>
      <DialogActions>
        {selectedCard && (
          <Button onClick={() => props.handleOK(level, selectedCard)}>
            OK
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
}
