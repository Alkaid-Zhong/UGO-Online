import { snackbar } from "@/store/app";

const message = (message: string) => {
  snackbar.show = true;
  snackbar.text = message;
  snackbar.color = "blue"
};

const success = (message: string) => {
  snackbar.show = true;
  snackbar.text = message;
  snackbar.color = "green"
};

const error = (message: string) => {
  snackbar.show = true;
  snackbar.text = message;
  snackbar.color = "red"
};

const warning = (message: string) => {
  snackbar.show = true;
  snackbar.text = message;
  snackbar.color = "yellow"
};

export default {
  message,
  success,
  error,
  warning
};