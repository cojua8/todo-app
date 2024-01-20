<script>
  import { onMount } from "svelte";

  export let name;
  export let errors;
  export let type;
  export let labelText;

  let inputElement;
  onMount(() => {
    inputElement.type = type;
  });
</script>

<div class="my-1 flex flex-col w-3/4">
  <label for={name} class="pl-1">{labelText}</label>
  <input {name} class="border rounded p-1" bind:this={inputElement} />
  {#if errors}
    <p class="text-red-500">{errors}</p>
  {/if}
</div>
