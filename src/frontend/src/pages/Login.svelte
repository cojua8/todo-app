<script>
  import LoginForm from "../lib/LoginForm.svelte";
  import page from "page";
  import { loggedUser } from "../stores/UserStore";
  import Button from "../lib/basics/Button.svelte";

  if ($loggedUser) {
    page.redirect("/dashboard");
  }
</script>

<LoginForm />
<br />
<Button on:click={() => page.redirect("/signup")} class="w-32">Signup</Button>
