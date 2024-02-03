<script>
  import page from "page";
  import SignupForm from "../lib/SignupForm.svelte";
  import { loggedUser } from "../stores/UserStores";

  if ($loggedUser) {
    page.redirect("/dashboard");
  }
</script>

<SignupForm />
