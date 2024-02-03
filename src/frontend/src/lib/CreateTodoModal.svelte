<script>
  import { bind } from "svelte-simple-modal";
  import { getUserTodos } from "../services/TodoApi";
  import { createTodoModal } from "../stores/ModalStores";
  import { todos } from "../stores/TodoStores";
  import { loggedUser } from "../stores/UserStores";
  import CreateTodoForm from "./CreateTodoForm.svelte";
  import Button from "./basics/Button.svelte";
  import Modal from "./basics/Modal.svelte";

  const handleSubmit = async () => {
    createTodoModal.set(null);
    todos.set(await (await getUserTodos($loggedUser.id)).json());
  };
</script>

<Modal modal={$createTodoModal}>
  <Button
    on:click={() =>
      createTodoModal.set(bind(CreateTodoForm, { onSubmit: handleSubmit }))}
  >
    Create New Todo
  </Button>
</Modal>
