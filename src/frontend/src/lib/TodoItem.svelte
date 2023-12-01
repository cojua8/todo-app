<script>
  export let id;
  export let owner_id;
  export let description;
  export let due_date;
  export let completed;
  export let date_created;
</script>

<div class="m-2 px-2 border rounded">
  <div class="flex flex-row flex-grow justify-between align-middle">
    <p>{description}</p>
    <p>{due_date}</p>
    <p>{date_created}</p>
    <p>{completed ? "✅" : "❌"}</p>
  </div>
</div>
