<script>
  import { selectedTodo } from "../stores/TodoStore";
  import TodoListItem from "./TodoListItem.svelte";

  export let todos = [];
</script>

<ul class="w-3/5">
  {#each todos.toSorted( (a, b) => a.dateCreated.localeCompare(b.dateCreated) ) as todo}
    <li>
      <TodoListItem on:click={() => selectedTodo.set(todo)} {...todo} />
    </li>
  {/each}
</ul>
