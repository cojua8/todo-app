<script>
  export let form;
</script>

<div class="border rounded w-2/5 {$$props.class}}">
  <form use:form={form} class="p-2 flex flex-col flex-grow items-center">
    <slot />
  </form>
</div>
