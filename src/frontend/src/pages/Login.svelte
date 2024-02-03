<script>
  import page from "page";
  import LoginForm from "../lib/LoginForm.svelte";
  import Button from "../lib/basics/Button.svelte";
  import { loggedUser } from "../stores/UserStores";

  if ($loggedUser) {
    page.redirect("/dashboard");
  }
</script>

<LoginForm />
<br />
<Button on:click={() => page.redirect("/signup")} class="w-32">Signup</Button>
