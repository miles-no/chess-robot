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
import { ChangeEvent, useState } from "react";

interface alertProps {
  open: boolean;
  stockfishLevel: number;
  handleOK: (level: number, selectedCard: boolean, name: string) => void;
}

export default function PreGame(props: alertProps) {
  const [level, setLevel] = useState(1);
  const [selectedCard, setSelectedCard] = useState<boolean | null>(null);
  const [name, setName] = useState<string>("");

  const handleBackdropClick = (event: React.MouseEvent<HTMLDivElement>) => {
    event.stopPropagation();
  };

  const handleLevelChange = (e: ChangeEvent<HTMLInputElement>) => {
    let value = Number(e.target.value);

    if (value < 1) {
      value = 1;
    } else if (value > 20) {
      value = 20;
    }

    setLevel(value);
  };
  const handleCardClick = (value: boolean) => {
    setSelectedCard(value);
  };
  const renderCard = (
    image: string,
    altText: string,
    cardText: string,
    value: boolean
  ) => (
    <Card
      sx={{
        width: 200,
        textAlign: "center",
        border: "3px",
        borderRadius: "16px",
      }}
    >
      <CardActionArea onClick={() => handleCardClick(value)}>
        <CardMedia
          sx={{ padding: "2em 2em 0em 0em", objectFit: "contain" }}
          component="img"
          height="100"
          image={image}
          alt={altText}
        />
        <CardContent>
          <Typography
            gutterBottom
            variant="h5"
            component="div"
            sx={{
              color: selectedCard === value ? "lightgreen" : "black",
            }}
          >
            {cardText}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );

  return (
    <Dialog
      open={props.open}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
      onClick={handleBackdropClick}
      disableEscapeKeyDown
      PaperProps={{
        sx: {
          overflow: "auto",
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
          padding: "1em 2em 0em 2em",
          margin: "0 auto",
          display: "flex",
          alignContent: "center",
          justifyContent: "center",
          width: "100%",
        }}
        container
        spacing={0}
      >
        <Box
          sx={{
            width: "100%",
            textAlign: "center",
          }}
        >
          <Typography sx={{ textAlign: "center" }}>Enter your name</Typography>
          <TextField
            id="outlined-controlled"
            value={name}
            onChange={(event) => {
              setName(event.target.value);
            }}
          />
        </Box>
        <Grid item sx={{ padding: "1em" }}>
          {renderCard("assets/images/king_w.png", "White piece", "White", true)}
        </Grid>
        <Grid item sx={{ padding: "1em" }}>
          {renderCard(
            "assets/images/king_b.png",
            "Black piece",
            "Black",
            false
          )}
        </Grid>
        <Box sx={{ paddingTop: "1em" }}>
          <Typography sx={{ textAlign: "center" }}>
            Set stockfish level (1-20)
          </Typography>
          <TextField
            value={level}
            type="number"
            inputProps={{ min: 1, max: 20 }}
            onChange={handleLevelChange}
          ></TextField>
          {level <= 8 ? (
            <Typography sx={{ textAlign: "center", color: "green" }}>
              Easy
            </Typography>
          ) : level <= 15 && level > 8 ? (
            <Typography sx={{ textAlign: "center", color: "orange" }}>
              Medium
            </Typography>
          ) : level === 20 ? (
            <Typography sx={{ textAlign: "center", color: "red" }}>
              Hardest
            </Typography>
          ) : (
            <Typography sx={{ textAlign: "center", color: "#ff4500" }}>
              Hard
            </Typography>
          )}
        </Box>
      </Grid>
      <DialogActions>
        {selectedCard !== null && (
          <Button onClick={() => props.handleOK(level, selectedCard, name)}>
            OK
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
}
