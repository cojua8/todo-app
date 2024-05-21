import { writable } from "svelte/store";

export const loggedUser = writable(
  JSON.parse(localStorage.getItem("loggedUser")),
);

loggedUser.subscribe((value) => {
  localStorage.setItem("loggedUser", JSON.stringify(value));
});
