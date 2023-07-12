import {
  Card,
  CardActionArea,
  CardContent,
  CardMedia,
  Dialog,
  DialogTitle,
  Grid,
  Typography,
} from "@mui/material";
//import blackKing from "../../../public/assets/images/king_b";
// import whiteKing from "../../../public/assets/images/king_w";
interface alertProps {
  handleWhite: () => void;
  handleBlack: () => void;
  open: boolean;
}

export default function ColorPicker(props: alertProps) {
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
          <Card sx={{ width: 200 }}>
            <CardActionArea onClick={props.handleWhite}>
              <CardMedia
                sx={{ padding: "0 2em 2em 0em", objectFit: "contain" }}
                component="img"
                height="100"
                //image={whiteKing}
                alt="White piece"
              />
              <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                  White
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>
        <Grid item>
          <Card sx={{ width: 200, backgroundColor: "black", color: "white" }}>
            <CardActionArea onClick={props.handleBlack}>
              <CardMedia
                sx={{ padding: "0 2em 2em 0em", objectFit: "contain" }}
                component="img"
                height="100"
                //image={blackKing}
                alt="black piece"
              />
              <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                  Black
                </Typography>
              </CardContent>
            </CardActionArea>
          </Card>
        </Grid>
      </Grid>
    </Dialog>
  );
}
