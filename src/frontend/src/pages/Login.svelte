<script>
  import LoginForm from "../lib/LoginForm.svelte";
  import page from "page";
</script>

<LoginForm />
<button on:click={() => page.redirect("/signup")}>Signup</button>
