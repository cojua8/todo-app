<script>
  import { bind } from "svelte-simple-modal";
  import { getUserTodos } from "../services/TodoApi";
  import { editTodoModal } from "../stores/ModalStores";
  import { selectedTodo, todos } from "../stores/TodoStores";
  import { loggedUser } from "../stores/UserStores";
  import EditTodoForm from "./EditTodoForm.svelte";
  import Modal from "./basics/Modal.svelte";

  const handleSubmit = async () => {
    editTodoModal.set(null);
    todos.set(await (await getUserTodos($loggedUser.id)).json());
  };

  selectedTodo.subscribe((value) => {
    if (value) {
      editTodoModal.set(
        bind(EditTodoForm, { handleSubmit: handleSubmit, todo: value })
      );
    }
  });
</script>

<Modal modal={$editTodoModal}></Modal>
