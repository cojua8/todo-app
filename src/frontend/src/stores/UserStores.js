import { writable } from "svelte/store";

const loggedUserStorage = "loggedUser";

export const loggedUser = writable(
  JSON.parse(localStorage.getItem(loggedUserStorage)),
);

loggedUser.subscribe((value) => {
  localStorage.setItem(loggedUserStorage, JSON.stringify(value));
});
