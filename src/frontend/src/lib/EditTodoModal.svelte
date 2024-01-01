<script>
  import { selectedTodo } from "../stores/TodoStore";
  import EditTodoForm from "./EditTodoForm.svelte";
  import Modal from "./basics/Modal.svelte";
</script>

<Modal
  on:click={() => selectedTodo.set(null)}
  on:keydown={(event) => event.key === "Escape" && selectedTodo.set(null)}
  class="w-3/5"
>
  <EditTodoForm todo={$selectedTodo} />
</Modal>
