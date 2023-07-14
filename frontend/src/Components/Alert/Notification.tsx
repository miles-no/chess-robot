import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
} from "@mui/material";

interface alertProps {
  alertTitle: string;
  message: string;
  handleOK: () => void;
  open: boolean;
}

export default function AlertComponent(props: alertProps) {
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
    >
      <DialogTitle id="alert-dialog-title">{props.alertTitle}</DialogTitle>
      <DialogContent>
        <DialogContentText id="alert-dialog-description">
          {props.message}
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={props.handleOK} autoFocus>
          OK
        </Button>
      </DialogActions>
    </Dialog>
  );
}
