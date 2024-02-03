<script>
  import { Modal } from "svelte-simple-modal";

  export let modal;
</script>

<Modal show={modal} closeButton={false}>
  <slot />
</Modal>
