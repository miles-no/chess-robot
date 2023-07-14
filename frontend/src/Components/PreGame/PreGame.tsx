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

interface alertProps {
  open: boolean;
  stockfishLevel: number;
  handleOK: (level: number, selectedCard: boolean) => void;
}

export default function PreGame(props: alertProps) {
  const [level, setLevel] = useState(1);
  const [selectedCard, setSelectedCard] = useState<boolean | null>(null);

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
        },
      }}
    >
      <DialogTitle
        id="alert-dialog-title"
        sx={{ textAlign: "center", padding: "2em 0 0 0" }}
      >
        Select your preferred options
      </DialogTitle>
      <Grid
        sx={{
          padding: "2em",
          margin: "0 auto",
          display: "flex",
          alignContent: "center",
          justifyContent: "center",
          width: "100%",
        }}
        container
        spacing={0}
      >
        <Grid item sx={{ padding: "1em" }}>
          <Card
            sx={{
              width: 200,
              textAlign: "center",
              border: "3px",
              borderRadius: "16px",
            }}
          >
            <CardActionArea
              onClick={() => {
                setSelectedCard(true);
              }}
            >
              <CardMedia
                sx={{ padding: "2em 2em 0em 0em", objectFit: "contain" }}
                component="img"
                height="100"
                image="assets/images/king_w.png"
                alt="White piece"
              />
              <CardContent>
                <Typography
                  gutterBottom
                  variant="h5"
                  component="div"
                  sx={{
                    color: selectedCard === true ? "lightgreen" : "black",
                  }}
                >
                  White
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>
        <Grid item sx={{ padding: "1em" }}>
          <Card
            sx={{
              width: 200,
              textAlign: "center",
              border: "3px",
              borderRadius: "16px",
            }}
          >
            <CardActionArea
              onClick={() => {
                setSelectedCard(false);
              }}
            >
              <CardMedia
                sx={{ padding: "2em 2em 0em 0em", objectFit: "contain" }}
                component="img"
                height="100"
                image="assets/images/king_b.png"
                alt="black piece"
              />
              <CardContent>
                <Typography
                  gutterBottom
                  variant="h5"
                  component="div"
                  sx={{
                    color: selectedCard === false ? "lightgreen" : "black",
                  }}
                >
                  Black
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>
        <Box sx={{ paddingTop: "1em" }}>
          <Typography sx={{ textAlign: "center" }}>
            Set stockfish level (1-20)
          </Typography>
          <TextField
            value={level}
            type="number"
            inputProps={{ min: 1, max: 20 }}
            onChange={(e) => setLevel(Number(e.target.value))}
          />
        </Box>
      </Grid>
      <DialogActions>
        {selectedCard !== null && (
          <Button onClick={() => props.handleOK(level, selectedCard)}>
            OK
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
}
