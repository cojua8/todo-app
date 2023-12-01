<script>
  import page from "page";

  import { loggedUser } from "../stores/UserStore";
  import { onMount } from "svelte";
  import { getUserTodos } from "../services/TodoApi";
  import TodoItem from "../lib/TodoItem.svelte";
  import Button from "../lib/basics/Button.svelte";

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

<ul class="w-3/5">
  {#each todos as todo}
    <li>
      <TodoItem {...todo} />
    </li>
  {/each}
</ul>
<br />
<Button on:click={logout}>Logout</Button>
