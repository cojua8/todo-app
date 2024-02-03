<script>
  import { validator } from "@felte/validator-yup";
  import { createForm } from "felte";
  import page from "page";
  import * as yup from "yup";
  import { loginUser } from "../services/TodoApi";
  import { loggedUser } from "../stores/UserStores";
  import Form from "./formBase/Form.svelte";
  import FormButton from "./formBase/FormButton.svelte";
  import FormItem from "./formBase/FormItem.svelte";

  let submitErrorMsg = undefined;
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
      submitErrorMsg = undefined;
      let response = await loginUser(values);
      switch (response.status) {
        case 200:
          loggedUser.set(await response.json());
          return;
        case 400:
          throw "Wrong username or password";
        default:
          console.log("Unknown error");
      }
    },
    onSuccess: () => {
      page.redirect("/dashboard");
    },
    onError: async (result) => {
      submitErrorMsg = result;
    },
  });
</script>

<Form {form} class="w-2/5">
  <FormItem
    name="username"
    labelText="Username"
    type="text"
    errors={$errors.username}
  />
  <FormItem
    name="password"
    labelText="Password"
    type="password"
    errors={$errors.password}
  />
  <br />
  {#if submitErrorMsg}
    <p class="text-red-500">{submitErrorMsg}</p>
  {/if}
  <FormButton>Login</FormButton>
</Form>
