<script>
  import { todos } from "../stores/TodoStores";
  import TodoListItem from "./TodoListItem.svelte";
</script>

<ul class="w-3/5">
  {#each $todos.toSorted( (a, b) => a.dateCreated.localeCompare(b.dateCreated) ) as todo}
    <li>
      <TodoListItem {todo} />
    </li>
  {/each}
</ul>
