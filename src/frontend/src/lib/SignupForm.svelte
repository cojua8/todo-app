<script>
  import page from "page";
  import { createForm } from "svelte-forms-lib";
  import * as yup from "yup";

  const { form, errors, handleChange, handleSubmit } = createForm({
    initialValues: {
      email: "xfvxfgd",
      username: "xfvxfgd",
      password: "dfgdfgdf",
      confirmPassword: "dfgdfgfdfddf",
    },
    onSubmit: (values) => {
      console.log(values);
      page.redirect("/dashboard");
    },
    validationSchema: yup.object().shape({
      email: yup.string().email().required("Email is required"),
      username: yup.string().required("Username is required"),
      password: yup.string().required("Password is required"),
      confirmPassword: yup.string().required("Password is required"),
    }),
    validate: (values) => {
      let errors = {};

      if (values.password != values.confirmPassword) {
        errors.confirmPassword = "Passwords do not match";
      }

      return errors;
    },
  });
</script>

<form on:submit={handleSubmit}>
  <label for="email">email</label>
  <input
    id="email"
    name="email"
    type="email"
    on:change={handleChange}
    bind:value={$form.email}
  />
  {#if $errors.email}
    <p>{$errors.email}</p>
  {/if}

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

  <label for="confirmPassword">confirmPassword</label>
  <input
    id="confirmPassword"
    name="confirmPassword"
    type="password"
    on:change={handleChange}
    bind:value={$form.confirmPassword}
  />
  {#if $errors.confirmPassword}
    <p>{$errors.confirmPassword}</p>
  {/if}

  <button type="submit">Submit</button>
</form>
