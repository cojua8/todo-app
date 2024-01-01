<script>
  import page from "page";
  import { selectedTodo } from "../stores/TodoStore";

  import { loggedUser } from "../stores/UserStore";
  import { onMount } from "svelte";
  import { getUserTodos } from "../services/TodoApi";
  import Button from "../lib/basics/Button.svelte";
  import TodoListing from "../lib/TodoListing.svelte";
  import EditTodoModal from "../lib/EditTodoModal.svelte";
  import CreateTodoModal from "../lib/CreateTodoModal.svelte";

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

  //every time selectedTodo changes, we fetch the todos again (it is supposed that the user has changed something)
  selectedTodo.subscribe(async () => {
    let response = await getUserTodos($loggedUser.id);
    todos = await response.json();
  });

  let createTodo = false;
</script>

<Button on:click={() => (createTodo = true)}>Create new</Button>

<TodoListing {todos} />
<br />
<Button on:click={logout}>Logout</Button>

{#if createTodo}
  <CreateTodoModal />
{/if}

{#if $selectedTodo}
  <EditTodoModal />
{/if}
