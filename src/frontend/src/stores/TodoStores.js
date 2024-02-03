import { writable } from "svelte/store";

export const selectedTodo = writable(null);
export const todos = writable([]);
