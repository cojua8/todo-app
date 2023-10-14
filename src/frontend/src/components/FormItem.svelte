<script>
  import { onMount } from "svelte";

  import StatusMessage from "./StatusMessage.svelte";

  export let name;
  export let labelText;
  export let type;
  export let placeholder;
  export let value;
  export let message;

  let inputElement;
  onMount(() => {
    inputElement.type = type;
  });
</script>

<div class="mb-4">
  <label class="block text-gray-700 text-sm font-bold mb-2" for={name}>
    {labelText}
  </label>
  <input
    class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
    id={name}
    {placeholder}
    bind:value
    bind:this={inputElement}
  />
</div>
<StatusMessage {message} type="ERROR" />
