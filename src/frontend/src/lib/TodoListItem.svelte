<script>
  export let description;
  export let dueDate;
  export let completed;
  export let dateCreated;
</script>

<div class="m-2 px-2 h-10 border rounded flex items-center">
  <div class="flex flex-row flex-grow justify-between">
    <p>{description}</p>
    <p>{dueDate}</p>
    <p>{dateCreated}</p>
    <p>{completed ? "✅" : "❌"}</p>
  </div>
  <button on:click>edit</button>
</div>
