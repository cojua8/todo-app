<script>
  import page from "page";

  import { loggedUser } from "../stores/UserStore";
  import { onMount } from "svelte";
  import { getUserTodos } from "../services/TodoApi";
  import TodoItem from "../lib/TodoItem.svelte";

  let todos = [];

  onMount(async () => {
    if (!$loggedUser) {
      page.redirect("/");
      console.log("no logged user");
      return;
    }

    todos = await (await getUserTodos($loggedUser.id)).json();
  });

  const logout = () => {
    page.redirect("/");
    loggedUser.set(null);
  };
</script>

<div class="flex flex-col">
  <ul class="flex flex-col items-center">
    {#each todos as todo}
      <li class="w-1/2">
        <TodoItem {...todo} />
      </li>
    {/each}
  </ul>
  <br />
  <button on:click={logout} class="px-3 py-1 border rounded w-52 self-center"
    >Logout</button
  >
</div>
