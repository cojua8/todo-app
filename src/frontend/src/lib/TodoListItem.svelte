<script>
  import { updateTodoItem } from "../services/TodoApi";

  export let todo;

  const toggleCompleted = async () => {
    let updatedTodo = { ...todo, completed: !todo.completed };

    await updateTodoItem(updatedTodo);
    // how to tell dashboard to reload the todos?
    //this is a workaround (loses coupling with real data)
    todo.completed = !todo.completed;
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
  <button on:click>edit</button>
</div>
