<script>
  import { getUserTodos, updateTodoItem } from "../services/TodoApi";
  import { selectedTodo, todos } from "../stores/TodoStores";
  import { loggedUser } from "../stores/UserStores";

  export let todo;

  const toggleCompleted = async () => {
    let updatedTodo = { ...todo, completed: !todo.completed };

    await updateTodoItem(updatedTodo);

    todos.set(await (await getUserTodos($loggedUser.id)).json());
  };
</script>

<div class="m-2 px-2 h-10 border rounded flex items-center">
  <div class="flex flex-row flex-grow justify-between">
    <p>{todo.description}</p>
    <p>{todo.dueDate}</p>
    <p>{todo.dateCreated}</p>
    <button on:click={() => toggleCompleted()}>
      {todo.completed ? "✅" : "❌"}
    </button>
  </div>
  <button on:click={() => selectedTodo.set(todo)}>edit</button>
</div>
