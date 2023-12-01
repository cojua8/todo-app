<script>
  import page from "page";
  import { createForm } from "felte";
  import { validator } from "@felte/validator-yup";
  import * as yup from "yup";
  import { loginUser } from "../services/TodoApi";
  import { loggedUser } from "../stores/UserStore";

  const { form, errors } = createForm({
    initialValues: {
      username: "theusername3",
      password: "password",
    },
    extend: validator({
      schema: yup.object().shape({
        username: yup.string().required("Username is required"),
        password: yup.string().required("Password is required"),
      }),
    }),
    onSubmit: async (values) => {
      let response = await loginUser(values);
      switch (response.status) {
        case 200:
          loggedUser.set(await response.json());
          return;
        case 400:
          throw await response.json();
        default:
          console.log("Unknown error");
      }
    },
    onSuccess: () => {
      page.redirect("/dashboard");
    },
    onError: async ({ result }) => {
      alert(result);
    },
  });
</script>

<form use:form>
  <label for="username">username</label>
  <input name="username" />
  {#if $errors.username}
    <p>{$errors.username}</p>
  {/if}

  <label for="password">password</label>
  <input name="password" type="password" />
  {#if $errors.password}
    <p>{$errors.password}</p>
  {/if}

  <button type="submit">Submit</button>
</form>
