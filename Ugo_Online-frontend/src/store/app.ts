import { reactive } from "vue";

export const snackbar = reactive({
  show: false,
  text: "",
  color: "green",
  timeout: 3000,
});