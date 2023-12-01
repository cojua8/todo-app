<script>
  import page from "page";
  import SignupForm from "../lib/SignupForm.svelte";
  import { loggedUser } from "../stores/UserStore";

  let user;
  loggedUser.subscribe((value) => {
    user = value;
  });

  if (user) {
    page.redirect("/dashboard");
  }
</script>

<SignupForm />
