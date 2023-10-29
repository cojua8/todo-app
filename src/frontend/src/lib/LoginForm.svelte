<script>
  import page from "page";
  import { createForm } from "svelte-forms-lib";
  import * as yup from "yup";

  const { form, errors, handleChange, handleSubmit } = createForm({
    initialValues: {
      username: "xfvxfgd",
      password: "dfgdfgdf",
    },
    onSubmit: (values) => {
      console.log(values);
      page.redirect("/dashboard");
    },
    validationSchema: yup.object().shape({
      username: yup.string().required("Username is required"),
      password: yup.string().required("Password is required"),
    }),
  });
</script>

<form on:submit={handleSubmit}>
  <label for="username">username</label>
  <input
    id="username"
    name="username"
    on:change={handleChange}
    bind:value={$form.username}
  />
  {#if $errors.username}
    <p>{$errors.username}</p>
  {/if}

  <label for="password">password</label>
  <input
    id="password"
    name="password"
    type="password"
    on:change={handleChange}
    bind:value={$form.password}
  />
  {#if $errors.password}
    <p>{$errors.password}</p>
  {/if}

  <button type="submit">Submit</button>
</form>
