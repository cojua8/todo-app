<script>
  import page from "page";

  import { onMount } from "svelte";
  import CreateTodoModal from "../lib/CreateTodoModal.svelte";
  import EditTodoModal from "../lib/EditTodoModal.svelte";
  import TodoListing from "../lib/TodoListing.svelte";
  import Button from "../lib/basics/Button.svelte";
  import { getUserTodos } from "../services/TodoApi";
  import { todos } from "../stores/TodoStores";
  import { loggedUser } from "../stores/UserStores";

  onMount(async () => {
    if (!$loggedUser) {
      page.redirect("/");
      console.log("no logged user");
      return;
    }

    todos.set(await (await getUserTodos($loggedUser.id)).json());
  });

  const logout = () => {
    page.redirect("/");
    loggedUser.set(null);
  };
</script>

<CreateTodoModal />

<EditTodoModal />

<TodoListing />
<br />
<Button on:click={logout}>Logout</Button>
