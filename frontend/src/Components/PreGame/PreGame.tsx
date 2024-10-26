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
  const [submitted, setSubmitted] =
    useState(false); /*Field to indicate name is empty on submission */

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
        width: "100%",
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
          <TextField
            label="Enter your name"
            id="outlined-controlled"
            value={name}
            onChange={(event) => {
              setName(event.target.value);
            }}
            error={
              submitted && (name.trim() === "" || !/^[A-Za-z\s]+$/.test(name))
            }
            helperText={
              submitted && name.trim() === ""
                ? "Name cannot be empty"
                : submitted && !/^[A-Za-z\s]+$/.test(name)
                ? "Name should only include alphabetic characters"
                : ""
            }
          />
        </Box>
        <Box sx={{ width: "100%", textAlign: "center", padding: "1em" }}>
          {renderCard(
            "assets/images/king_b.png",
            "Black piece",
            "Black",
            false
          )}
        </Box>
        <Box sx={{ paddingTop: "1em" }}>
          <Typography sx={{ textAlign: "center" }}>
            Set stockfish level (1-20)
          </Typography>
          <TextField
            sx={{ width: "100%" }}
            value={level}
            type="number"
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
          <Button
            onClick={() => {
              setSubmitted(true);

              if (name.trim() !== "" && /^[A-Za-z\s]+$/.test(name)) {
                /*Name to only include alphabetic characters*/
                props.handleOK(level, selectedCard, name);
              }
            }}
          >
            OK
          </Button>
        )}
      </DialogActions>
    </Dialog>
  );
}
