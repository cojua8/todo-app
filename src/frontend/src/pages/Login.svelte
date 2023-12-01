<script>
  import LoginForm from "../lib/LoginForm.svelte";
  import page from "page";
  import { loggedUser } from "../stores/UserStore";

  if ($loggedUser) {
    page.redirect("/dashboard");
  }
</script>

<div>
  <LoginForm />
  <button on:click={() => page.redirect("/signup")}>Signup</button>
</div>
